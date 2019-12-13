# -*- coding: UTF-8 -*-
from ..cm.utils import is_exist, is_empty
from ..db.obj import C
from .db import E, Q

def sql_sel(auth, apikey):
    if is_empty(auth) and is_empty(apikey):
        return None
    print(E.POSTGRE)
    cls = load_DB_Class(get_db_info(auth, apikey))
    if cls is None:
        return None

    cls.add_db_method_mode(Q.SELECT)
    return cls.method()

def sql_ins(auth):
    cls = load_DB_Class(get_db_info(auth, apikey))
    if cls is None:
        return None

    cls.add_db_method_mode(Q.INSERT)
    return cls.method()

def sql_upd(auth):
    cls = load_DB_Class(get_db_info(auth, apikey))
    if cls is None:
        return None

    cls.add_db_method_mode(Q.UPDATE)
    return cls.method()

def sql_del(auth):
    cls = load_DB_Class(get_db_info(auth, apikey))
    if cls is None:
        return None

    cls.add_db_method_mode(Q.DELETE)
    return cls.method()

def load_DB_Class(auth):
    # auth['engine_mode'] = E.POSTGRE
    emode = auth['engine_mode']
    if emode is None:
        print('Connection engine mode is required!!!')
        return None

    cls = C()
    cls.add_info(auth)
    cls.add_engine_mode(emode)
    cls.add_query('select 1')
    print(cls.__dict__)
    return cls

def get_db_info(auth, apikey):
    if is_empty(auth) and is_empty(apikey):
        return None
    
    # Username and Password Or API KEY
    # Check In Common Database get Result to [obj]
    result = {}
    result['host'] = 'sc-p-db'
    result['port'] = 5432
    result['database']='scapp'
    result['user']='postgres'
    result['password']='postgres080' 

    result['engine_mode'] = E.POSTGRE

    return result