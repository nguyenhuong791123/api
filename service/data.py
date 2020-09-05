import copy

from utils.cm.utils import *
from utils.cm.system import *
from utils.db.engine.db import DB
from utils.db.auth.server import Server, ServerInfo
from utils.db.crm.page import Page

def getServiceSaveData(page, cId, uId):
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

def getServiceUpdateData(page, cId, uId):
    print(page)
    print(cId)
    print(uId)
    return page
