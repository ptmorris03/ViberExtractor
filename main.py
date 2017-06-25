import sqlite3
import argparse

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def execute(conn, query):
    cur = conn.cursor()
    cur.execute(query)

    return cur.fetchall()

def main():
    parser = argparse.ArgumentParser(description='Extract messages from a supplied sqlite database of Viber message logs.')
    parser.add_argument('db_location', metavar="db_location", type=str, help='the location of the viber database')
    parser.add_argument('--out', default="out.txt", type=str, help="the optional name and location of the text file to output")
    parser.add_argument('--chatname', default="", type=str, help="the optional name of the chat to extract messages from")
    parser.add_argument('--starttime', default=0, type=int, help="the optional start time to filter from, as an integer UNIX timestamp")
    parser.add_argument('--endtime', default=999999999999, type=int, help="the optional end time to filter to, as an integer UNIX timestamp")

    args = parser.parse_args()

    db_location = args.db_location
    out_file = args.out
    chat_name = args.chatname
    unixtime_start = args.starttime
    unixtime_end = args.endtime

    conn = create_connection(db_location)

    #if a chat name is supplied, get the chat_id from the desired chat name
    if chat_name:
        chat_id = execute(conn, "select ChatID from ChatInfo where instr(UPPER(Name), UPPER('" + chat_name + "')) > 0")
        if len(chat_id) > 0:
            chat_id = chat_id[0][0]
        else:
            #If no group chat was found with that name, check contacts for an individual name
            contact_id = execute(conn, "select ContactID from Contact where instr(UPPER(Name), Upper('" + chat_name + "')) OR instr(UPPER(ClientName), UPPER('" + chat_name + "'))")

            #if a contact was found, get the chat they appear in which has no other contacts
            if len(contact_id) > 0:
                contact_id = contact_id[0][0]
                
                #get the chat with contact_id in it that only has 2 people (you + contact)
                chat_id = execute(conn, "select c1.ChatID from ChatRelation c1 where c1.ContactID='" + str(contact_id) + "' and (select COUNT(*) from ChatRelation c2 where c2.ChatID=c1.ChatID)=2")
                if len(chat_id) > 0:
                    chat_id = chat_id[0][0]
                else:
                    print("Found contact with name " + chat_name + ", but no chat found.")
                    return
            else:
                print("Couldn't find that chat name in groups or contacts. Make sure it's spelled correctly.")
                return


    #get all messages
    #if a chat_id is supplied, get only messages with chat_id
    chat_str = " where ChatId='" + str(chat_id) + "'" if chat_name else ""
    messages = execute(conn, "select timestamp, EventId, datetime(timestamp, 'unixepoch'), Body, Direction from EventInfo" + chat_str + " order by timestamp")

    #filter messages to the specified time range (0 to 999999999999 if none specified)
    messages = [x[1:] for x in messages if int(x[0]) > unixtime_start and int(x[0]) < unixtime_end]

    #get the id of the contact that sent each message
    ids = [execute(conn, "select ContactID from Events where EventID='" + str(x[0]) + "'")[0][0] for x in messages]

    #get the name and ClientName fields for the sender of each message
    names = [execute(conn, "select Name, ClientName from Contact where ContactID='" + str(x) + "'")[0] for x in ids]

    #pick whichever of the Name and ClientName fields isn't empty
    final = [[y[1], x[1] if x[1] is not None else x[0], y[2], y[3]] for x, y in zip(names, messages)]

    #filter out the "like" messages, which just contain a ~13+ digit code for the message liked.
    final = [x for x in final if not (str(x[2]).isnumeric() and len(x[2]) > 13)]

    #print the messages to a text file
    with open(out_file, "w", encoding='utf-8') as f:
        for message in final:
            message = [str(message[0])[11:], ("From: " if int(message[3]) == 0 else "To:   ") + str(message[1]).ljust(22, ' '), str(message[2])]
            f.write(", ".join(message) + "\n")

if __name__ == "__main__":
    main()