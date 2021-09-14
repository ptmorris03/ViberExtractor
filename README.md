# UPDATE: Here is an improved fork 
https://github.com/gsakkis/ViberExtractor

# ViberExtractor
A python 3 script for extracting messages from Viber Desktop's sqlite message database into a text file.

If you use Viber Desktop, all your messages are stored in a sqlite database. In windows, this is usually located at: C:\Users\*USERANAME*\AppData\Roaming\ViberPC\*YOURPHONE#*\viber.db

to extract messages from viber.db with this script, download and run main.py

supports optional cmd line arguments for location of output file, chat name to extract, and UNIX start/end times to filter messages by

# Example Usage:

python3 main.py viber.db --out "outfile.txt" --chatname "Sally"
