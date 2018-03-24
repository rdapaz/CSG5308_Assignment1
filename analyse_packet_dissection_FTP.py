import re
import json
import pprint


def pretty_printer(o):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(o)

with open(r'/home/rdapaz/Desktop/packet_dissection_FTP.json', 'r') as f:
    data = json.load(f)


def ftp_request_getter(ftp_chain):
    for k, v in ftp_chain.items():
        arg, command = '', ''
        if type(v) != dict:
            if k == 'ftp.request.arg':
                arg = k
            elif k == 'ftp.request.command':
                command = k
            if any([arg, command]):
                return [arg, command]
            else:
                return None
        elif type(v) == dict:
            ftp_request_getter(v)




my_data = []
for entry in data:
    frame_number = entry["_source"]["layers"]["frame"]["frame.number"]
    epoch = entry["_source"]["layers"]["frame"]["frame.time_epoch"]
    source_ip = entry["_source"]["layers"]["ip"]["ip.src"]
    destn_ip = entry["_source"]["layers"]["ip"]["ip.dst"]
    pretty_printer(entry["_source"]["layers"]["ftp"])
    ftp_arg = ftp_request_getter(entry["_source"]["layers"]["ftp"])[0] if ftp_request_getter(entry["_source"]["layers"]["ftp"]) else ''
    ftp_command = ftp_request_getter(entry["_source"]["layers"]["ftp"])[1] if ftp_request_getter(entry["_source"]["layers"]["ftp"]) else ''
    if source_ip == '192.168.1.5':
        my_data.append([frame_number, source_ip, destn_ip, ftp_arg, ftp_command])

# entry["_source"]["layers"]["ip"]["ip.dst"]
# destn_ips = [x[2] for x in my_data]
# refs= [x[3] for x in my_data]
pretty_printer(my_data)
# pretty_printer(sorted(list(set(destn_ips))))
# pretty_printer(sorted(list(set(refs))))


'''
referer_rex = re.compile(r'Referer\:\s+(.*)(?=\\r\\n)')

urls = []
for item in referer_rex.findall(data):
    urls.append(item)

for entry in list(set(urls)):
    print(entry)
'''