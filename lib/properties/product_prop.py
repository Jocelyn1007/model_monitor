import configparser

cfgpath = 'lib/properties/product_map.ini'
conf = configparser.ConfigParser()
conf.read(cfgpath, encoding='utf-8')
product_map = {k: v for k, v in conf.items('product_map')}