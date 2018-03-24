import re
import json
import pprint


def pretty_printer(o):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(o)

with open(r'/home/rdapaz/Desktop/packet_dissection.json', 'r') as f:
    data = json.load(f)

my_data = []
for entry in data:
    frame_number = entry["_source"]["layers"]["frame"]["frame.number"]
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
        my_data.append([frame_number, source_ip, destn_ip, referrer, uri])

entry["_source"]["layers"]["ip"]["ip.dst"]
destn_ips = [x[2] for x in my_data]
refs= [x[3] for x in my_data]
pretty_printer(my_data)
pretty_printer(sorted(list(set(destn_ips))))
pretty_printer(sorted(list(set(refs))))


'''
referer_rex = re.compile(r'Referer\:\s+(.*)(?=\\r\\n)')

urls = []
for item in referer_rex.findall(data):
    urls.append(item)

for entry in list(set(urls)):
    print(entry)
'''