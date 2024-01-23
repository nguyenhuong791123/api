import copy

from utils.cm.utils import *
from utils.cm.system import *
from utils.db.engine.db import DB
from utils.db.auth.server import Server, ServerInfo
from utils.db.crm.page import Page

def getServiceSaveData(page, cId, uId):
    result = None
    try:
        conn = DB(get_common_db_info())
        conn = Server(conn)
        server = conn.get_server_by_type(cId, 0)
        if server is not None:
            server = ServerInfo(many=False).dump(server)
            conn = DB(get_db_info(server))
            pconn = Page(conn)
            data = pconn.save_datas(page, cId, uId)
            if is_empty(data) == False and is_integer(data[0]) == True:
                cs = None
                fs = page['form']
                for f in fs:
                    schema = []
                    if isinstance(f['object'], list):
                        for obj in f['object']:
                            fc = {}
                            fc['object'] = obj
                            schema.append(fc)
                    else:
                        schema.append(f)

                    for s in schema:
                        kp = s['object']['schema']['properties']
                        csdata = s['object']['data']
                        print(csdata)
                        for key, value in kp.items():
                            if key.endswith('_customize') and is_exist(csdata, key):
                                print(key)
                                if cs == None:
                                    cs = {}
                                ct = key[0:key.find('_')]
                                if ct == 'text':
                                    ct = 'varchar'
                                elif ct == 'month':
                                    ct = 'date'
                                elif ct in [ 'textarea', 'editor' ]:
                                    ct = 'text'
                                elif ct in [ 'file', 'image' ]:
                                    ct = 'file'
                                elif ct in [ 'number', 'checkbox', 'radio', 'select' ]:
                                    if ct == 'number':
                                        ct = 'double'
                                    else:
                                        ct = 'integer'
                                if is_exist(cs, ct + '_field_datas'):
                                    cs[ct + '_field_datas'].append({ 'properties_name': key, 'value': csdata[key] })
                                else:
                                    cs[ct + '_field_datas'] = [{ 'properties_name': key, 'value': csdata[key] }]
                                print(ct)
                                print(cs)
                if cs:
                    pconn.save_customize_datas(page['page_id'], data[0], cs)
                    # for key, value in cs.items():
                    #     pconn.save_customize_datas(page['page_id'], data[0], key, value)

            result = {}
            result[page['page_id_seq']] = data[0]
        else:
            result = { 'error': 'Not Server Info!!!'}
    except Exception as ex:
        result = { 'error': str(ex) }
    finally:
        if conn is not None:
            conn.close_session()

    return result

def getServiceUpdateData(page, cId, uId, rId):
    print(page)
    print(rId)
    print(cId)
    print(uId)
    result = None
    try:
        conn = DB(get_common_db_info())
        conn = Server(conn)
        server = conn.get_server_by_type(cId, 0)
        if server is not None:
            server = ServerInfo(many=False).dump(server)
            conn = DB(get_db_info(server))
            pconn = Page(conn)
            data = pconn.update_datas(page, cId, uId, rId)
            # print(data)
            if is_empty(data) == False and is_integer(data[0]) == True:
                cs = None
                us = None
                fs = page['form']
                for f in fs:
                    schema = []
                    if isinstance(f['object'], list):
                        for obj in f['object']:
                            fc = {}
                            fc['object'] = obj
                            schema.append(fc)
                    else:
                        schema.append(f)

                    for s in schema:
                        kp = s['object']['schema']['properties']
                        csdata = s['object']['data']
                        for key, value in kp.items():
                            if key.endswith('_customize') and is_exist(csdata, key):
                                ct = key[0:key.find('_')]
                                if ct == 'text':
                                    ct = 'varchar'
                                elif ct == 'month':
                                    ct = 'date'
                                elif ct in [ 'textarea', 'editor' ]:
                                    ct = 'text'
                                elif ct in [ 'file', 'image' ]:
                                    ct = 'file'
                                elif ct in [ 'number', 'checkbox', 'radio', 'select' ]:
                                    if ct == 'number':
                                        ct = 'double'
                                    else:
                                        ct = 'integer'

                                if is_exist(value, 'field_id') and is_integer(value['field_id']):
                                    if us == None:
                                        us = {}
                                    if is_exist(us, ct + '_field_datas'):
                                        us[ct + '_field_datas'].append({ 'properties_name': key, 'value': csdata[key], 'field_id': value['field_id'] })
                                    else:
                                        us[ct + '_field_datas'] = [{ 'properties_name': key, 'value': csdata[key], 'field_id': value['field_id'] }]
                                else:
                                    if cs == None:
                                        cs = {}
                                    if is_exist(cs, ct + '_field_datas'):
                                        cs[ct + '_field_datas'].append({ 'properties_name': key, 'value': csdata[key] })
                                    else:
                                        cs[ct + '_field_datas'] = [{ 'properties_name': key, 'value': csdata[key] }]
                if cs:
                    pconn.save_customize_datas(page['page_id'], data[0], cs)
                if us:
                    pconn.update_customize_datas(us)
            result = {}
            result[page['page_id_seq']] = page['page_id']
        else:
            result = { 'error': 'Not Server Info!!!'}
    except Exception as ex:
        result = { 'error': str(ex) }
    finally:
        if conn is not None:
            conn.close_session()

    return result

def getServiceDeleteFieldData(cId, uId, rId, fields):
    print(field)
    print(cId)
    print(uId)
    return field
