import configparser

cfgpath = 'lib/properties/dbs.ini'
conf = configparser.ConfigParser()
conf.read(cfgpath, encoding='utf-8')

bigdb = {k: v for k, v in conf.items('bigDB')}
bigdb['port'] = int(conf.get('bigDB', 'port'))