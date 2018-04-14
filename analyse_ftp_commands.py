import re
import sqlite3
import os
import sys
import json

current_path = os.path.dirname(sys.argv[0])
os.chdir(current_path)
ROOT = r'.' 
JSON_FOLDER = os.path.join(ROOT, 'json_dumps')

ftp_commands = {   
                'CWD': 'Change working directory: Allows the user to specify a different '
                       'directory for the file transfer\n',
                'DELE': 'Deletes a file on the FTP server\n',
                'LIST': 'Lists content of current working directory\n',
                'PASS': 'Specifies the password for the user given previously by the USER '
                        'command\n',
                'PORT': 'Used to tell the FTP server that the client wants to accept an '
                        'active data connection on a specific port number\n',
                'QUIT': 'Terminates the FTP session and closes the control connection\n',
                'RETR': 'Tells the server to send the user a file\n',
                'RMD':  'Removes a directory on the server\n',
                'STOR': 'Sends a file to the server\n',
                'SYST': 'Requests that the server send the client information about the '
                        "server's operating system\n",
                'TYPE': 'Specifies the data type for the file being transferred (A = '
                        'ASCII, I = Binary)\n',
                'USER': 'Identifies the user attempting to establish an FTP session\n'
                }

file_path = os.path.join(JSON_FOLDER, 'packet_dissection_FTP.json')
path_to_db = os.path.join(ROOT, 'capture_events.sqlite3' )
conn = sqlite3.connect(path_to_db)
cur = conn.cursor()
sql = """
    SELECT dt, command FROM "ftp_events"
    WHERE LENGTH(command) > 0
    """
cur.execute(sql)
data = []
for row in cur.fetchall():
    dt, command = row
    m = re.search(r'([A-Z]+)(\s(.*))?', command)
    if m:
        cmd = m.group(1)
        arg = '' if not m.group(2) else m.group(2)
        desc = ftp_commands[cmd]
        if cmd in ('PORT', 'PASV'):
            h1, h2, h3, h4, p1, p2 = arg.split(',')
            added_info = f"ip_addr={h1}.{h2}.{h3}.{h4}, port={256*int(p1)+int(p2)}"
            desc = f"{desc}{added_info}"
        elif len(arg) > 0:
            desc = f"{desc}In this case: '{arg.strip()}'"
        data.append(['', dt, command, desc])

with open(os.path.join(JSON_FOLDER, 'ftp_data_for_table.json'), 'w') as fout:
    json.dump(data, fout, indent=True)