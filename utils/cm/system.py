import json

o = open('json/system.json')
j = json.load(o)

def get_common_db_info():
    return '{u}:{w}@{h}:{p}/{d}'.format(**{
            'h': j['db']['host']
            ,'p': j['db']['port']
            ,'u': j['db']['username']
            ,'w': j['db']['password']
            ,'d': j['db']['database']
        })

def get_db_info(info):
    return '{u}:{w}@{h}:{p}/{d}'.format(**{
            'h': info['host']
            ,'p': info['port']
            ,'u': info['username']
            ,'w': info['password']
            ,'d': info['database']
        })
