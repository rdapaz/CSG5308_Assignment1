import json
import pprint
import datetime
import pytz
import sqlite3
import os
import sys


def pretty_printer(o):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(o)


def dt_from_epoch(epoch):
    my_timezone = pytz.timezone('Australia/Perth')
    return datetime.datetime.fromtimestamp(float(epoch)). \
        astimezone(my_timezone).strftime('%Y-%m-%d %H:%M:%S')


current_path = os.path.dirname(sys.argv[0])
os.chdir(current_path)
ROOT = r'.' 
JSON_FOLDER = os.path.join(ROOT, 'json_dumps')

file_path = os.path.join(JSON_FOLDER, 'packet_dissection_HTTP.json')
path_to_db = os.path.join(ROOT, 'capture_events.sqlite3' )


with open(file_path, 'r') as f:
    data = json.load(f)


my_data = []
for entry in data:
    frame_number = entry["_source"]["layers"]["frame"]["frame.number"]
    epoch = entry["_source"]["layers"]["frame"]["frame.time_epoch"]
    dt = dt_from_epoch(epoch)
    source_ip = entry["_source"]["layers"]["ip"]["ip.src"]
    destn_ip = entry["_source"]["layers"]["ip"]["ip.dst"]
    referrer = ''
    full_uri = ''
    try:
        referrer = entry["_source"]["layers"]["http"]["http.referer"]
    except:
        pass
    try:
        uri = entry["_source"]["layers"]["http"]["http.request.full_uri"]
    except:
        pass
    if source_ip == '192.168.1.5':
        my_data.append([frame_number, dt, source_ip, destn_ip, referrer, uri])

conn = sqlite3.connect(path_to_db)
cur = conn.cursor()
sql = 'DROP TABLE IF EXISTS http_events'
cur.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS http_events (
    id integer PRIMARY KEY,
    frame_number long,
    dt TEXT,
    source_ip TEXT,
    destn_ip TEXT,
    referrer TEXT,
    uri TEXT
    )
    """
cur.execute(sql)

sql = """
    INSERT INTO http_events (
        frame_number,
        dt,
        source_ip,
        destn_ip,
        referrer,
        uri
        )
    VALUES (
    ?, ?, ?, ?, ?, ?)
    """

for entry in my_data:
    cur.execute(sql, entry)
    conn.commit()

pretty_printer(my_data)