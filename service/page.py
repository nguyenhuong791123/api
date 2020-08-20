import copy

from utils.cm.utils import *
from utils.cm.system import *
from utils.db.engine.db import DB
from utils.db.auth.server import Server, ServerInfo
from utils.db.crm.page import Page, PageMenu, PageForm, PageMenuSchema, PageFormSchema, PageMenuSchema
from utils.db.crm.pageRel import PageRel, PageRelSchema
from utils.db.crm.label import Label
from utils.db.crm.label import Label
from utils.db.crm.form import Form, FormSchema
from utils.db.crm.schema import Schema, SchemaSchema
from utils.db.crm.ui import Ui
from utils.db.crm.defaultdata import DefaultData
from utils.db.crm.properties import Properties
from utils.db.crm.editobject import EditObject
from utils.db.crm.options import Options

def setServicePage(page, cId, uId):
    uconn = None
    pconn = None
    lconn = None
    fconn = None
    sconn = None
    osccon = None
    eoconn = None
    psconn = None
    uiconn = None
    dconn = None
    result = None
    try:
        conn = DB(get_common_db_info())
        conn = Server(conn)
        server = conn.get_server_by_type(cId, 0)
        if server is not None:
            server = ServerInfo(many=False).dump(server)
            uconn = DB(get_db_info(server))
            pconn = Page(uconn)
            page['page_order'] = pconn.get_max_order_by()
            pconn.__json__(page, cId, uId)
            pconn.add(pconn)
            result = PageMenuSchema(many=False).dump(pconn)
            result['items'] = []

            pl = []
            plsconn = Label(uconn)
            pln = {}
            pln['properties_name'] = str(result['page_id'])
            pln['object_label'] = { 'ja': page['page_name'] }
            plsconn.__json__(pln)
            pl.append(plsconn)

            forms = page['form']
            for f in forms:
                fconn = Form(uconn)
                fconn.__json__(f, result['page_id'])
                fconn.add(fconn)
                form = FormSchema(many=False).dump(fconn)

                schema = []
                if isinstance(f['object'], list):
                    for obj in f['object']:
                        fc = copy.copy(f)
                        fc['object'] = {}
                        fc['object'] = obj
                        schema.append(fc)
                else:
                    schema.append(f)

                for obj in schema:
                    if is_exist(obj['object'], 'schema') == False:
                        continue

                    sconn = Schema(uconn)
                    sconn.__json__(obj['object']['schema'], form['form_id'])
                    sconn.add(sconn)
                    s = SchemaSchema(many=False).dump(sconn)
                    if s['schema_id'] is not None and obj['object'] is not None:
                        if is_exist(obj['object'], 'schema') == True and is_exist(obj['object']['schema'], 'obj') == True:
                            eos = []
                            eoconn = EditObject(uconn)
                            eo = {}
                            eo['properties_name'] = s['schema_key']
                            eo['schema_id'] = s['schema_id']
                            eo['edit_type'] = 1
                            eo['value'] = obj['object']['schema']['obj']
                            eoconn.__json__(eo)
                            eos.append(eoconn)

                            if is_exist(obj['object']['schema']['obj'], 'label') == True:
                                plsconn = Label(uconn) 
                                pln = {}
                                pln['properties_name'] = s['schema_key']
                                pln['object_label'] = obj['object']['schema']['obj']['label']
                                plsconn.__json__(pln)
                                pl.append(plsconn)

                        pls = []
                        pts = []
                        os = []
                        psconn = Properties(uconn)
                        plsconn = Label(uconn)
                        pp = obj['object']['schema']['properties']
                        for key in pp.keys():
                            if is_exist(pp[key], 'options') == True:
                                if is_exist(pp[key], 'option_target') == False or is_empty(pp[key]['option_target']) == True:
                                    osccon = Options(uconn)
                                    osccon.add_patition(key)
                                    pts.append(key)
                                    pp[key]['option_target'] = key
                                    idx = 0
                                    for opt in pp[key]['options']:
                                        osccon = Options(uconn)
                                        o = {}
                                        o['option_name'] = key
                                        o['option_code'] = opt['value']
                                        o['option_value'] = opt['label']
                                        o['option_order'] = idx
                                        o['company_id'] = cId
                                        osccon.__json__(o)
                                        os.append(osccon)
                                        idx += 1

                            psconn = Properties(uconn)
                            p = {}
                            p['properties_name'] = key
                            p['schema_id'] = s['schema_id']
                            p['value'] = pp[key]
                            psconn.__json__(p)
                            pl.append(psconn)

                            if is_exist(pp[key], 'obj') == True:
                                plsconn = Label(uconn) 
                                pln = {}
                                pln['properties_name'] = key
                                pln['object_label'] = pp[key]['obj']['label']
                                plsconn.__json__(pln)
                                pl.append(plsconn)

                                eoconn = EditObject(uconn)
                                eo = {}
                                eo['properties_name'] = key
                                eo['schema_id'] = s['schema_id']
                                eo['edit_type'] = 1
                                eo['value'] = pp[key]['obj']
                                eoconn.__json__(eo)
                                eos.append(eoconn)

                            if pl:
                                psconn.add_all(pl)
                            if pls:
                                plsconn.add_all(pls)
                            if eos:
                                eoconn.add_all(eos)
                            if os:
                                osccon.add_all(os)

                        if is_exist(obj['object'], 'ui') == True:
                            ul = []
                            uiconn = Ui(uconn)
                            ui = obj['object']['ui']
                            for key in ui.keys():
                                uiconn = Ui(uconn)
                                u = {}
                                u['properties_name'] = key
                                u['schema_id'] = s['schema_id']
                                u['value'] = ui[key]
                                uiconn.__json__(u)
                                ul.append(uiconn)
                            if ul:
                                uiconn.add_all(ul)

                        if is_exist(obj['object'], 'data') == True:
                            dl = []
                            dconn = DefaultData(uconn)
                            dt = obj['object']['data']
                            for key in dt.keys():
                                dconn = DefaultData(uconn)
                                d = {}
                                d['properties_name'] = key
                                d['schema_id'] = s['schema_id']
                                d['value'] = dt[key]
                                dconn.__json__(d)
                                dl.append(dconn)
                            if dl:
                                dconn.add_all(dl)

        else:
            result = { 'error': 'Not Server Info!!!'}
    except Exception as ex:
        if osccon is not None and pts:
            for pt in pts:
                osccon.drop_patition(pt)
        if uiconn is not None and is_exist(s, 'schema_id') == True:
            uiconn.delete(s['schema_id'])
        if dconn is not None and is_exist(s, 'schema_id') == True:
            dconn.delete(s['schema_id'])
        if psconn is not None and is_exist(s, 'schema_id') == True:
            psconn.delete(s['schema_id'])
        if eoconn is not None and is_exist(s, 'schema_id') == True:
            eoconn.delete(s['schema_id'])
        if sconn is not None and is_exist(form, 'form_id') == True:
            sconn.delete(form['form_id'])
        if fconn is not None and is_exist(result, 'page_id') == True:
            fconn.delete(result['page_id'])
        if lconn is not None and is_exist(result, 'page_id') == True:
            lconn.delete(result['page_id'], 1)
        if pconn is not None and is_exist(result, 'page_id') == True:
            pconn.delete(result['page_id'])

        result = { 'error': str(ex) }
    finally:
        if uconn is not None:
            uconn.close_session()

    return result

def getServicePage(cId, pId, language):
    conn = None
    result = None
    try:
        conn = DB(get_common_db_info())
        conn = Server(conn)
        server = conn.get_server_by_type(cId, 0)
        if server is not None:
            server = ServerInfo(many=False).dump(server)
            conn = DB(get_db_info(server))
            pconn = PageForm(conn)
            page = pconn.get_form_fields(cId, pId, language)
            result = PageFormSchema(many=False).dump(page)

            forms = result['form']
            for f in forms:
                if f['object_type'] == 'div':
                    obj = copy.copy(f['object'][0])
                    f['object'] = obj
        else:
            result = { 'error': 'Not Server Info!!!'}
    except Exception as ex:
        result = { 'error': str(ex) }
    finally:
        if conn is not None:
            conn.close_session()

    return result

def setServiceGroupPage(page, cId, uId):
    conn = None
    pconn = None
    lconn = None
    prconn = None
    result = None
    try:
        conn = DB(get_common_db_info())
        conn = Server(conn)
        server = conn.get_server_by_type(cId, 0)
        if server is not None:
            server = ServerInfo(many=False).dump(server)
            conn = DB(get_db_info(server))
            pconn = Page(conn)
            pconn.__json__(page, cId, uId)
            pconn.add(pconn)
            result = PageMenuSchema(many=False).dump(pconn)
            pconn.update_all(page['items'])

            plsconn = Label(conn)
            pln = {}
            pln['properties_name'] = str(result['page_id'])
            pln['object_label'] = { 'ja': page['page_name'] }
            plsconn.__json__(pln)
            plsconn.add(plsconn)

            pIds = [p["page_id"] for p in page['items']]
            for pId in pIds:
                prconn = PageRel(conn)
                prconn.delete(pId, False)
                prconn.__json__(result['page_id'], pId)
                prconn.add(prconn)

            sconn = PageMenu(conn, 'items')
            menu = sconn.get_menus(cId, 'ja')
            result = PageMenuSchema(many=True).dump(menu)
        else:
            result = { 'error': 'Not Server Info!!!'}

    except Exception as ex:
        if prconn is not None and is_exist(result, 'page_id') == True:
            prconn.delete(result['page_id'], True)
        if lconn is not None and is_exist(result, 'page_id') == True:
            lconn.delete(result['page_id'], 1)
        if pconn is not None and is_exist(result, 'page_id') == True:
            pconn.delete(result['page_id'])

        result = { 'error': str(ex) }
    finally:
        if conn is not None:
            conn.close_session()

    return result

def updateServicePage(page, cId):
    result = None
    try:
        conn = DB(get_common_db_info())
        conn = Server(conn)
        server = conn.get_server_by_type(cId, 0)
        if server is not None:
            server = ServerInfo(many=False).dump(server)
            conn = DB(get_db_info(server))
            pconn = Page(conn)
            pconn.update(page)
            result = page

        else:
            result = { 'error': 'Not Server Info!!!'}
    except Exception as ex:
        result = { 'error': str(ex) }
    finally:
        if conn is not None:
            conn.close_session()

    return result

def updateServicePages(pages, cId):
    result = None
    try:
        conn = DB(get_common_db_info())
        conn = Server(conn)
        server = conn.get_server_by_type(cId, 0)
        if server is not None:
            server = ServerInfo(many=False).dump(server)
            conn = DB(get_db_info(server))
            pconn = Page(conn)
            pconn.update_all(pages)

            for page in pages:
                if (is_exist(page, 'items') == True
                    and is_empty(page['items']) == False
                    and is_empty(page['items'][0]) == False):
                    pconn.update_all(page['items'])
                    pIds = [p["page_id"] for p in page['items']]
                    pgconn = PageRel(conn)
                    pgconn.delete(page['page_id'], True)
                    for pId in pIds:
                        prconn = PageRel(conn)
                        prconn.delete(pId, False)
                        prconn.__json__(page['page_id'], pId)
                        prconn.add(prconn)

            sconn = PageMenu(conn, 'items')
            menu = sconn.get_menus(cId, 'ja')
            result = PageMenuSchema(many=True).dump(menu)
        else:
            result = { 'error': 'Not Server Info!!!'}
    except Exception as ex:
        result = { 'error': str(ex) }
    finally:
        if conn is not None:
            conn.close_session()

    return result

def deleteServicePage(page, cId):
    try:
        conn = DB(get_common_db_info())
        conn = Server(conn)
        server = conn.get_server_by_type(cId, 0)
        if server is not None:
            server = ServerInfo(many=False).dump(server)
            conn = DB(get_db_info(server))
            if is_empty(page['page_key']) == False and page['page_key'].startswith('table_'):
                sconn = Schema(conn)
                ss = sconn.get(page['page_id'])
                for s in ss:
                    psconn = Properties(conn)
                    psconn.delete(s.schema_id)
                    uiconn = Ui(conn)
                    uiconn.delete(s.schema_id)
                    dconn = DefaultData(conn)
                    dconn.delete(s.schema_id)
                sconn.delete(page['page_id'])

            pconn = Page(conn)
            prconn = PageRel(conn)
            pIds = prconn.gets(page['page_id'])
            if page['page_auth'] is None and is_empty(pIds) == False:
                order = pconn.get_max_order_by()[0]
                for idx in range(len(pIds)):
                    pr = PageRelSchema(many=False).dump(pIds[idx])
                    pconn.update({ 'page_id': pr['page_id'], 'page_order': (order + idx) })
                prconn.delete(page['page_id'], True)
            pconn.delete(page['page_id'])

            sconn = PageMenu(conn, 'items')
            menu = sconn.get_menus(cId, 'ja')
            result = PageMenuSchema(many=True).dump(menu)
        else:
            result = { 'error': 'Not Server Info!!!'}
    except Exception as ex:
        result = { 'error': str(ex) }
            # result = str(ex)
    finally:
        if conn is not None:
            conn.close_session()

    return result
