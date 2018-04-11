import json
import pprint
import os
import datetime
import pytz
import sqlite3

def pretty_printer(o):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(o)


ROOT_FOLDER = r'C:\Users\rdapaz\Documents\CSG5138_ass1'
file_path = os.path.join(ROOT_FOLDER, 'json_dumps', 'ftp_commands.json')
path_to_db = os.path.join(ROOT_FOLDER, 'capture_events.sqlite3' )


conn = sqlite3.connect(path_to_db)
cur = conn.cursor()

sql = """
    SELECT
        frame_number,
        dt,
        source_ip,
        destn_ip,
        command,
        response
    FROM ftp_events
    """

cur.execute(sql)

my_data = []

try:
    for row in cur.fetchall():
        frame_number, dt, source_ip, destn_ip, command, response = row
        command_response = f"Command:\n{command}" if command else f"Response:\n{response}"
        my_data.append([frame_number, dt, source_ip, destn_ip, command_response])
except:
    pass

pretty_printer(my_data)

with open(file_path, 'w') as f:
    json.dump(my_data, f, indent=True)