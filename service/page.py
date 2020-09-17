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
from utils.db.query.page import getProperties, getLabels, getUis

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
    pl = None
    pls = None
    eos = None
    ul = None
    dl = None
    # customize = []
    try:
        conn = DB(get_common_db_info())
        conn = Server(conn)
        server = conn.get_server_by_type(cId, 0)
        if server is not None:
            server = ServerInfo(many=False).dump(server)
            uconn = DB(get_db_info(server))
            pconn = Page(uconn)
            if is_integer(page['page_id']) == True:
                pconn.update(page)
                result = page
                pdplsconn = Label(uconn)
                pdplsconn.delete_page_id(page['page_id'])
            else:
                page['page_order'] = pconn.get_max_order_by()
                pconn.__json__(page, cId, uId)
                pconn.add(pconn)
                result = PageMenuSchema(many=False).dump(pconn)
                result['items'] = []
                pk = result['page_key'] + '_' + '{0:07}'.format(result['page_id'])
                result['page_key'] = pk
                result['page_id_seq'] = 'integer_seq_id_' + pk.replace('customize.table_', '')
                pconn.update(result)

            ul = []
            dl = []
            pls = []
            plsconn = Label(uconn)
            pln = {}
            pln['schema_id'] = result['page_id']
            pln['properties_name'] = str(result['page_id'])
            pln['object_label'] = { 'ja': page['page_name'] }
            plsconn.__json__(pln)
            pls.append(plsconn)

            addIdSeq = True
            forms = page['form']
            for f in forms:
                fconn = Form(uconn)
                if is_exist(f, 'form_id') == True and is_integer(f['form_id']) == True:
                    form = f
                    fconn.update(form)
                else:
                    fconn.__json__(f, result['page_id'])
                    fconn.add(fconn)
                    form = FormSchema(many=False).dump(fconn)

                schema = []
                if isinstance(f['object'], list):
                    for obj in f['object']:
                        fc = {}
                        fc['object'] = obj
                        schema.append(fc)
                else:
                    schema.append(f)

                # print(schema)
                pl = []
                os = []
                pts = []
                eos = []
                for sc in schema:
                    if is_exist(sc['object'], 'schema') == False:
                        continue

                    sconn = Schema(uconn)
                    objschema = sc['object']['schema']
                    if is_exist(objschema, 'schema_id') == True and is_integer(objschema['schema_id']) == True:
                        s = objschema
                        sconn.update(s)
                    else:
                        sconn.__json__(objschema, form['form_id'])
                        sconn.add(sconn)
                        s = SchemaSchema(many=False).dump(sconn)

                    if is_integer(page['page_id']) == False and addIdSeq == True:
                        psconn = Properties(uconn)
                        psconn.__json__(getProperties(result['page_id_seq'], s['schema_id']))
                        pl.append(psconn)
                        plsconn = Label(uconn)
                        plsconn.__json__(getLabels(result['page_id_seq'], s['schema_id'], { 'en': 'ID', 'ja': 'ID', 'vi':'ID' }))
                        pls.append(plsconn)
                        uiconn = Ui(uconn)
                        uiconn.__json__(getUis(result['page_id_seq'], s['schema_id'], { 'ui:widget': 'hidden' }))
                        ul.append(uiconn)

                        tbl = result['page_id_seq'].replace('integer_seq_id_', '')
                        createdId = 'integer_' + tbl + '_created_id'
                        psconn = Properties(uconn)
                        psconn.__json__(getProperties(createdId, s['schema_id']))
                        pl.append(psconn)
                        plsconn = Label(uconn)
                        plsconn.__json__(getLabels(createdId, s['schema_id'], { 'en': 'Author', 'ja': '作成者', 'vi':'Author' }))
                        pls.append(plsconn)
                        uiconn = Ui(uconn)
                        uiconn.__json__(getUis(createdId, s['schema_id'], { 'ui:widget': 'hidden' }))
                        ul.append(uiconn)
                        createdTime = 'datetime_' + tbl + '_created_time'
                        psconn = Properties(uconn)
                        psconn.__json__(getProperties(createdTime, s['schema_id']))
                        pl.append(psconn)
                        plsconn = Label(uconn)
                        plsconn.__json__(getLabels(createdTime, s['schema_id'], { 'en': 'Created date', 'ja': '作成日時', 'vi':'Created date' }))
                        pls.append(plsconn)
                        uiconn = Ui(uconn)
                        uiconn.__json__(getUis(createdTime, s['schema_id'], { 'ui:widget': 'hidden' }))
                        ul.append(uiconn)

                        updatedId = 'integer_' + tbl + '_updated_id'
                        psconn = Properties(uconn)
                        psconn.__json__(getProperties(updatedId, s['schema_id']))
                        pl.append(psconn)
                        plsconn = Label(uconn)
                        plsconn.__json__(getLabels(updatedId, s['schema_id'], { 'en': 'Changer', 'ja': '更新者', 'vi':'Changer' }))
                        pls.append(plsconn)
                        uiconn = Ui(uconn)
                        uiconn.__json__(getUis(updatedId, s['schema_id'], { 'ui:widget': 'hidden' }))
                        ul.append(uiconn)
                        updatedTime = 'datetime_' + tbl + '_updated_time'
                        psconn = Properties(uconn)
                        psconn.__json__(getProperties(updatedTime, s['schema_id']))
                        pl.append(psconn)
                        plsconn = Label(uconn)
                        plsconn.__json__(getLabels(updatedTime, s['schema_id'], { 'en': 'Updated date', 'ja': '更新日時', 'vi':'Updated date' }))
                        pls.append(plsconn)
                        uiconn = Ui(uconn)
                        uiconn.__json__(getUis(updatedTime, s['schema_id'], { 'ui:widget': 'hidden' }))
                        ul.append(uiconn)
                    addIdSeq = False

                    if s['schema_id'] is not None and sc['object'] is not None:
                        if is_exist(objschema, 'obj') == True:
                            eoconn = EditObject(uconn)
                            eo = {}
                            eo['properties_name'] = s['schema_key']
                            eo['schema_id'] = s['schema_id']
                            eo['edit_type'] = 1
                            eo['value'] = objschema['obj']
                            eoconn.__json__(eo)
                            eos.append(eoconn)

                            if is_exist(objschema['obj'], 'label') == True:
                                plsconn = Label(uconn) 
                                pln = {}
                                pln['schema_id'] = s['schema_id']
                                pln['properties_name'] = s['schema_key']
                                pln['object_label'] = objschema['obj']['label']
                                plsconn.__json__(pln)
                                pls.append(plsconn)

                        psconn = Properties(uconn)
                        plsconn = Label(uconn)
                        pp = objschema['properties']
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
                            # if is_integer(page['page_id']) and key.endswith('_customize'):
                            #     customize.append(key)

                            if is_exist(pp[key], 'obj') == True and is_exist(pp[key]['obj'], 'label'):
                                plsconn = Label(uconn)
                                pln = {}
                                pln['schema_id'] = s['schema_id']
                                pln['properties_name'] = key
                                pln['object_label'] = pp[key]['obj']['label']
                                plsconn.__json__(pln)
                                pls.append(plsconn)

                                eoconn = EditObject(uconn)
                                eo = {}
                                eo['properties_name'] = key
                                eo['schema_id'] = s['schema_id']
                                eo['edit_type'] = 1
                                eo['value'] = pp[key]['obj']
                                eoconn.__json__(eo)
                                eos.append(eoconn)
                            if is_integer(page['page_id']) == True and key.find('_seq_id_') > 0:
                                plsconn = Label(uconn)
                                pln = {}
                                pln['schema_id'] = s['schema_id']
                                pln['properties_name'] = key
                                pln['object_label'] = { 'en': 'ID', 'ja': 'ID', 'vi':'ID' }
                                plsconn.__json__(pln)
                                pls.append(plsconn)

                        if is_exist(sc['object'], 'ui') == True:
                            uiconn = Ui(uconn)
                            ui = sc['object']['ui']
                            for key in ui.keys():
                                uiconn = Ui(uconn)
                                u = {}
                                u['properties_name'] = key
                                u['schema_id'] = s['schema_id']
                                u['value'] = ui[key]
                                uiconn.__json__(u)
                                ul.append(uiconn)

                        if is_exist(sc['object'], 'data') == True:
                            dconn = DefaultData(uconn)
                            dt = sc['object']['data']
                            for key in dt.keys():
                                dconn = DefaultData(uconn)
                                d = {}
                                d['properties_name'] = key
                                d['schema_id'] = s['schema_id']
                                d['value'] = dt[key]
                                dconn.__json__(d)
                                dl.append(dconn)

                        if pl:
                            dpsconn = Properties(uconn)
                            dpsconn.delete(s['schema_id'])
                        if pls:
                            dplsconn = Label(uconn)
                            dplsconn.delete(s['schema_id'])
                        if eos:
                            deoconn = EditObject(uconn)
                            deoconn.delete(s['schema_id'])
                        if os:
                            osccon.add_all(os)
                        if ul:
                            duiconn = Ui(uconn)
                            duiconn.delete(s['schema_id'])
                        if dl:
                            ddconn = DefaultData(uconn)
                            ddconn.delete(s['schema_id'])

                if pl:
                    psconn.add_all(pl)
                if pls:
                    plsconn.add_all(pls)
                if eos:
                    eoconn.add_all(eos)
                if ul:
                    uiconn.add_all(ul)
                if dl:
                    dconn.add_all(dl)

            page['page_key'] = result['page_key']
            if is_integer(page['page_id']) == False:
                pconn.create_table(page)
            # else:
            #     print(customize)
        else:
            result = { 'error': 'Not Server Info!!!'}
    except Exception as ex:
        if is_integer(page['page_id']) == False:
            if pl:
                psconn.delete(s['schema_id'])
            if pls:
                plsconn.delete_in_properties_name([d.properties_name for d in pls])
            if eos:
                eoconn.delete(s['schema_id'])
            if ul:
                uiconn.delete(s['schema_id'])
            if dl:
                dconn.delete(s['schema_id'])
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

def getServicePage(cId, pId, language, edit):
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
            if edit == True:
                page = pconn.get_edit_form_fields(cId, pId, language)
            else:
                page = pconn.get_form_fields(cId, pId, language)
            result = PageFormSchema(many=False).dump(page)

            forms = result['form']
            for f in forms:
                if f['object_type'] == 'div':
                    obj = copy.copy(f['object'][0])
                    f['object'] = obj
                elif f['object_type'] == 'tab' and isinstance(f['object'], list):
                    for o in f['object']:
                        o['schema']['tab_name'] = copy.copy(o['schema']['title'])
                        del o['schema']['title']
            # print(result)
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
            #page['page_layout'] = 0
            #page['page_open'] = 0
            pconn.__json__(page, cId, uId)
            pconn.add(pconn)
            result = PageMenuSchema(many=False).dump(pconn)
            pconn.update_all(page['items'])

            plsconn = Label(conn)
            pln = {}
            pln['schema_id'] = result['page_id']
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
            ls = []
            if is_empty(page['page_key']) == False and page['page_key'].startswith('customize.table_') == True:
                ls.append(str(page['page_id']))
                fconn = Form(conn)
                fs = fconn.get_by_page_id(page['page_id'])
                if fs is not None:
                    for f in fs:
                        sconn = Schema(conn)
                        ss = sconn.get_by_form_id(f.form_id)
                        if ss is not None:
                            for s in ss:
                                ls.append(s.schema_key)
                                psconn = Properties(conn)
                                ps = psconn.get_by_schema_id(s.schema_id)
                                for p in ps:
                                    ls.append(p.properties_name)
                                psconn.delete(s.schema_id)
                                uiconn = Ui(conn)
                                uiconn.delete(s.schema_id)
                                dconn = DefaultData(conn)
                                dconn.delete(s.schema_id)
                                eoconn = EditObject(conn)
                                eoconn.delete(s.schema_id)
                        sconn.delete(f.form_id)
                    plconn = Label(conn)
                    plconn.delete_in_properties_name(ls)
                    fconn.delete(page['page_id'])

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
