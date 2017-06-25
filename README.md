# ViberExtractor
A python 3 script for extracting messages from Viber Desktop's sqlite message database into a text file.

If you use Viber Desktop, all your messages are stored in a sqlite database. In windows, this is usually located at: C:\Users\*USERANAME*\AppData\Roaming\ViberPC\*YOURPHONE#*\viber.db

to extract messages from viber.db with this script, download and run main.py

# Example Usage:

python3 main.py viber.db --out "outfile.txt" --chatname "Sally"

# Example Output:

12:31:54, From: Sally    , bro what was that type of cheese you had at lunch?
14:44:56, From: Sally    , o sry wrong number
14:45:12, From: Sally    , but I mean if u have any cheese recommendations...
14:45:19, To  : Sally    , Not a cheese fan
14:45:31, From: Sally    , Then why am I still talking to you
