import json
import pprint
import os
import datetime
import pytz
import sqlite3
import sys


current_path = os.path.dirname(sys.argv[0])
os.chdir(current_path)
ROOT = r'.' 
JSON_FOLDER = os.path.join(ROOT, 'json_dumps')

file_path = os.path.join(JSON_FOLDER, 'packet_dissection_FTP.json')
path_to_db = os.path.join(ROOT, 'capture_events.sqlite3' )

with open(file_path, 'r') as f:
    data = json.load(f)


def pretty_printer(o):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(o)


def ftp_request_getter(ftp_chain):
    for k in ftp_chain.keys():
        if k == 'ftp.request':
            pass
        elif k == 'ftp.response':
            pass
        else:
            k = k.replace('\\r\\n', '')
            return k


def dt_from_epoch(epoch):
    my_timezone = pytz.timezone('Australia/Perth')
    return datetime.datetime.fromtimestamp(float(epoch)). \
        astimezone(my_timezone).strftime('%Y-%m-%d %H:%M:%S')


my_data = []
for entry in data:
    frame_number = entry["_source"]["layers"]["frame"]["frame.number"]
    epoch = entry["_source"]["layers"]["frame"]["frame.time_epoch"]
    dt = dt_from_epoch(epoch)
    source_ip = entry["_source"]["layers"]["ip"]["ip.src"]
    destn_ip = entry["_source"]["layers"]["ip"]["ip.dst"]
    cmd_resp = ftp_request_getter(entry["_source"]["layers"]["ftp"])
    command, response = '', ''
    if any(cmd_resp.startswith(x) for x in ['CWD', 'DELE', 'LIST', 'PASS', 
                    'PORT', 'QUIT', 'RETR', 'RMD', 'STOR', 'SYST', 'TYPE',
                    'USER']):
        command = cmd_resp
    else:
        response = cmd_resp
    my_data.append([frame_number, dt, source_ip, destn_ip, command, response])


conn = sqlite3.connect(path_to_db)
cur = conn.cursor()
sql = 'DROP TABLE IF EXISTS ftp_events'
cur.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS ftp_events (
    id integer PRIMARY KEY,
    frame_number long,
    dt TEXT,
    source_ip TEXT,
    destn_ip TEXT,
    command TEXT,
    response TEXT
    )
    """
cur.execute(sql)

sql = """
    INSERT INTO ftp_events (
        frame_number,
        dt,
        source_ip,
        destn_ip,
        command,
        response
        )
    VALUES (
    ?, ?, ?, ?, ?, ?)
    """

for entry in my_data:
    cur.execute(sql, entry)
    conn.commit()

pretty_printer(my_data)