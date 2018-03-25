def ftp_request_getter(ftp_chain):
    for k, v in ftp_chain.keys():
        print(k)
        if any(k.startswith(x) for x in ['CWD', 'DELE', 'LIST', 'PASS', 
                'PORT', 'QUIT', 'RETR', 'RMD', 'STOR', 'SYST', 'TYPE',
                'USER','150', '200', '215', '221', '226', '230', 
                '250', '331', '550']):
            if any(k.startswith(x) for x in ['CWD', 'DELE', 'LIST', 'PASS', 
                    'PORT', 'QUIT', 'RETR', 'RMD', 'STOR', 'SYST', 'TYPE',
                    'USER']):
                k = k.replace('\\r\\n', '')
                return k
            elif any(k.startswith(x) for x in ['150', '200', '215',
                '221', '226', '230', '250', '331', '550']):
                k = k.replace('\\r\\n', '')
                return k
                
