import json
from ...cm.utils import is_exist, is_empty, is_integer

def getSaveDatas(page, cId, uId):
    if is_exist(page, 'page_key') == False:
        return None

    tbl = page['page_key']
    idSeq = page['page_id_seq']
    fs = page['form']
    tbls = [ 'company.company_info', 'company.group_info', 'company.users_info', 'mente.page_info', 'system.api_info', 'system.server_info' ]
    fix = False
    istbl = tbl[(tbl.find('.')+1):]
    if tbl in tbls:
        fIdx = idSeq.find(tbl.split('.')[1]) + (len(tbl.split('.')[1]) + 1)
        idSeq = idSeq[fIdx:]
        fix = True
    else:
        idSeq = idSeq[(idSeq.find('_') + 1):]

    cols = ""
    vals = ""
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
            data = s['object']['data']
            for key, value in kp.items():
                if is_exist(data, key) == True and key.endswith('_customize') == False:
                    col = key
                    ct = key[0:key.find('_')]
                    if fix == True and is_exist(data, key) == True and is_empty(str(data[key])) == False:
                        fIdx = col.find(tbl.split('.')[1]) + (len(tbl.split('.')[1]) + 1)
                        col = key[fIdx:]
                    if is_empty(col) == False or is_empty(ct) == False:
                        cols += " %s," % (col)
                        if ct in [ 'integer', 'number', 'select', 'checkbox', 'radio' ]:
                            vals += " %s," % (data[key])
                        elif ct in [ 'image', 'file' ]:
                            vals += " '%s'," % (json.dumps(data[key]))
                        else:
                            vals += " '%s'," % (data[key])

    if is_empty(cols) == False and cols.endswith(','):
        cols = cols[0:len(cols)-1]
    if is_empty(cols) == False and vals.endswith(','):
        vals = vals[0:len(vals)-1]
    sql = " INSERT INTO %s(%s) VALUES(%s) RETURNING %s; " % (tbl, cols, vals, idSeq)
    print(sql)
    return " INSERT INTO %s(%s) VALUES(%s) RETURNING %s; " % (tbl, cols, vals, idSeq)

def getSaveCustomizeDatas(pId, rId, tbl, fields):
    if is_integer(pId) == False or is_integer(rId) == False or is_empty(tbl) == True or fields is None or len(fields) <= 0:
        return None
    print(fields)
    sql = " INSERT INTO customize.%s(page_id, row_id, properties_name, value) VALUES " % (tbl)
    ct = tbl[0:tbl.find('_')]
    for f in fields:
        if ct == 'file':
            sql += " (%s, %s, '%s', '%s')," % (pId, rId, f['properties_name'], json.dumps(f['value']))
        elif ct in [ 'integer', 'double' ]:
            sql += " (%s, %s, '%s', %s)," % (pId, rId, f['properties_name'], f['value'])
        else:
            sql += " (%s, %s, '%s', '%s')," % (pId, rId, f['properties_name'], f['value'])

    if is_empty(sql) == False and sql.endswith(','):
        sql = sql[0:len(sql)-1]
    sql += ";"
    print(sql)
    return sql

def getUpdateDatas(page, cId, uId, rId):
    if is_exist(page, 'page_key') == False:
        return None

    tbl = page['page_key']
    idSeq = page['page_id_seq']
    fs = page['form']
    tbls = [ 'company.company_info', 'company.group_info', 'company.users_info', 'mente.page_info', 'system.api_info', 'system.server_info' ]
    fix = False
    istbl = tbl[(tbl.find('.')+1):]
    if tbl in tbls:
        fIdx = idSeq.find(tbl.split('.')[1]) + (len(tbl.split('.')[1]) + 1)
        idSeq = idSeq[fIdx:]
        fix = True
    else:
        idSeq = idSeq[(idSeq.find('_') + 1):]

    cols = ""
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
            data = s['object']['data']
            for key, value in kp.items():
                if is_exist(data, key) == True and key.endswith('_customize') == False and key.endswith(idSeq) == False:
                    col = key
                    ct = key[0:key.find('_')]
                    if fix == True and is_exist(data, key) == True:
                        fIdx = col.find(tbl.split('.')[1]) + (len(tbl.split('.')[1]) + 1)
                        col = key[fIdx:]
                    if is_empty(col) == False or is_empty(ct) == False:
                        if ct in [ 'integer', 'number', 'select', 'checkbox', 'radio' ]:
                            cols += " %s=%s," % (col, data[key])
                        elif ct in [ 'image', 'file' ]:
                            cols += " %s='%s'," % (col, json.dumps(data[key]))
                        else:
                            cols += " %s='%s'," % (col, data[key])

    if is_empty(cols) == False and cols.endswith(','):
        cols = cols[0:len(cols)-1]
        # sql = " UPDATE %s SET %s WHERE %s=%s; " % (tbl, cols, idSeq, rId)
        # print(sql)
        return " UPDATE %s SET %s WHERE %s=%s; " % (tbl, cols, idSeq, rId)
    return None

def getUpdateCustomizeDatas(tbl, f):
    if is_empty(tbl) == True or is_empty(f) == True:
        return None

    print(f)
    sql = ""
    key = f['properties_name']
    ct = key[0:key.find('_')]
    if ct in [ 'integer', 'number', 'select', 'checkbox', 'radio' ]:
        sql += " UPDATE customize.%s SET value=%s WHERE field_id=%s; " % (tbl, f['value'], f['field_id'])
    elif ct in [ 'image', 'file' ]:
        sql += " UPDATE customize.%s SET value='%s' WHERE field_id=%s; " % (tbl, json.dumps(f['value']), f['field_id'])
    else:
        sql += " UPDATE customize.%s SET value='%s' WHERE field_id=%s; " % (tbl, f['value'], f['field_id'])
    return sql

def getDeleteFieldDatas(cId, pId, tbl, fields):
    sql = " DELETE FROM customize.%s WHERE %s.page_id=%s;" % (tbl, tbl, pId)
    sql += " AND text_field_datas.page_id IN (SELECT page_id FROM mente.page_info WHERE page_info.company_id=%s)" % (cId)
    if fields:
        sql += " AND text_field_datas.properties_name IN(%s) " % (",".join("'{0}'".format(e) for e in fields))
    return sql
