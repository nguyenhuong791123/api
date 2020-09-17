import copy
from ...cm.utils import is_exist, is_empty

def getMenuQuery():
    sql = " SELECT p.page_id, p.page_flag, p.page_key, p.page_open, p.page_order, p.page_auth::jsonb, l.object_label::jsonb->>:language AS page_name, json_agg(row_to_json(items)) AS items "
    sql += " FROM mente.page_info p "
    sql += " LEFT JOIN mente.label_info l ON l.properties_name=p.page_id::varchar AND l.schema_id=p.page_id "
    sql += " LEFT JOIN (SELECT pr.page_group_id, p1.page_id, p1.page_flag, p1.page_key, p1.page_order, p1.page_auth::jsonb, l1.object_label::jsonb->>:language AS page_name "
    sql += " FROM mente.page_info p1 "
    sql += " LEFT JOIN mente.label_info l1 ON l1.properties_name=p1.page_id::varchar AND l1.schema_id=p1.page_id "
    sql += " LEFT JOIN mente.page_group_rel pr ON pr.page_id=p1.page_id "
    sql += " WHERE p1.company_id=:cId AND p1.page_deleted=0 AND p1.page_key<>'mente.page_info') AS items ON items.page_group_id=p.page_id "
    sql += " WHERE p.company_id=:cId AND p.page_deleted=0 AND p.page_key<>'mente.page_info' "
    sql += " AND p.page_id NOT IN(SELECT page_id FROM mente.page_group_rel) "
    sql += " GROUP BY p.page_id, p.page_key, p.page_open, l.object_label ORDER BY p.page_order, p.page_id "
    return sql

def getPageFields(edit):
    sql = " SELECT p.page_id, p.page_key, p.page_id_seq, p.page_layout, p.page_open, p.page_auth::jsonb, l.object_label::jsonb->>:language AS page_name "
    sql += " ,json_agg( "
    sql += " json_build_object( "
    sql += " 'form_id', f.form_id, "
    sql += " 'className', f.class_name, "
    sql += " 'object_key', f.object_key, "
    sql += " 'object_type', f.object_type, "
    sql += " 'idx', f.idx, "
    sql += " 'object', (SELECT json_agg( "
    sql += " json_build_object( "
    sql += " 'schema', json_build_object( "
    sql += " 'schema_id', s.schema_id, "
    sql += " 'schema_type', s.schema_type, "
    sql += " 'schema_key', s.schema_key, "
    sql += " 'title', pll.object_label::jsonb->>:language, "
    sql += " 'type', s.object_type, "
    sql += " 'form_idx', f.idx, "
    sql += " 'idx', s.idx, "
    if edit == True:
        sql += " 'obj', COALESCE((SELECT eo.value::jsonb FROM mente.edit_object_info eo WHERE eo.schema_id=s.schema_id AND eo.properties_name=s.schema_key), '{}'::jsonb), "
    sql += " 'properties', COALESCE((SELECT json_object_agg(pp.properties_name, pp.value::jsonb || json_build_object('title', pl.object_label::jsonb->>:language)::jsonb "
    sql += " || json_build_object('properties_id', properties_id)::jsonb "
    if edit == True:
        sql += " || json_build_object('obj', COALESCE(eop.value::jsonb, '{}'::jsonb))::jsonb "
    sql += " ) FROM mente.properties_info pp LEFT JOIN mente.label_info pl ON pl.properties_name=pp.properties_name AND pl.schema_id=pp.schema_id "
    if edit == True:
        sql += " LEFT JOIN mente.edit_object_info eop ON eop.properties_name=pp.properties_name AND eop.schema_id=s.schema_id "
    sql += " WHERE pp.schema_id=s.schema_id)::jsonb, '{}'::jsonb) "
    sql += " ) "
    sql += " ,'ui', COALESCE((SELECT json_object_agg(u.properties_name, u.value) FROM mente.ui_info u WHERE u.schema_id=s.schema_id)::jsonb, '{}'::jsonb) "
    sql += " ,'data', COALESCE((SELECT json_object_agg(d.properties_name, d.value) FROM mente.default_data_info d WHERE d.schema_id=s.schema_id)::jsonb, '{}'::jsonb) "
    sql += " )) FROM mente.schema_info s "
    sql += " LEFT JOIN mente.label_info pll ON pll.properties_name=s.schema_key "
    sql += " WHERE s.form_id=f.form_id)) "
    sql += " ) AS form "
    sql += " FROM mente.page_info p "
    sql += " LEFT JOIN mente.form_info f ON f.page_id=p.page_id "
    sql += " LEFT JOIN mente.label_info l ON l.properties_name=p.page_id::varchar AND l.schema_id=p.page_id "
    sql += " WHERE p.company_id=:cId AND p.page_deleted=0 AND p.page_id=:pId "
    sql += " GROUP BY p.page_id, p.page_key, p.page_id_seq, p.page_layout, p.page_open, p.page_auth::jsonb, l.object_label "
    return sql

def getCreateTable(page):
    if is_exist(page, 'page_key') == False:
        return None

    tbl = page['page_key']
    colId = 'seq_id_' + tbl.replace('customize.table_', '')
    sql = " CREATE SEQUENCE customize.%s; " % (colId)
    sql += " CREATE TABLE %s (" % (tbl)
    sql += " %s INTEGER NOT NULL DEFAULT nextval('customize.%s'::regclass), " % (colId, colId)
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
        # print(schema)
        for s in schema:
            kp = s['object']['schema']['properties']
            for key, value in kp.items():
                ct = key[0:key.find('_')]
                required = 'NULL'
                if is_exist(kp[key]['obj'], 'required') == True and kp[key]['obj']['required'] == True:
                    required = 'NOT NULL'
                if ct in [ 'integer', 'checkbox', 'radio', 'select' ]:
                    if required == 'NULL':
                        sql += " %s INTEGER %s, " % (key, required)
                    else:
                        sql += " %s INTEGER %s DEFAULT 0, " % (key, required)
                elif ct in [ 'image', 'file' ]:
                    if required == 'NULL':
                        sql += " %s JSON %s, " % (key, required)
                    else:
                        sql += " %s JSON %s DEFAULT '{}', " % (key, required)
                elif ct == 'number':
                    if required == 'NULL':
                        sql += " %s DECIMAL(20, 3) %s, " % (key, required)
                    else:
                        sql += " %s DECIMAL(20, 3) %s DEFAULT 0, " % (key, required)
                elif ct == 'datetime':
                    if required == 'NULL':
                        sql += " %s TIMESTAMP %s, " % (key, required)
                    else:
                        sql += " %s TIMESTAMP %s DEFAULT CURRENT_TIMESTAMP, " % (key, required)
                elif ct == 'date' or ct == 'month':
                    if required == 'NULL':
                        sql += " %s DATE %s, " % (key, required)
                    else:
                        if ct == 'month':
                            sql += " %s DATE %s DEFAULT DATE(TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMM')), " % (key, required)
                        else:
                            sql += " %s DATE %s DEFAULT DATE(TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD')), " % (key, required)
                else:
                    length = 50
                    if ct == 'textarea':
                        length = 500
                    if is_exist(kp[key]['obj'], 'max_length') == True:
                        length = kp[key]['obj']['max_length']
                    if required == 'NULL':
                        sql += " %s VARCHAR(%d) %s, " % (key, length, required)
                    else:
                        sql += " %s VARCHAR(%d) %s DEFAULT '', " % (key, length, required)

    field = 'integer_' + tbl.replace('customize.table_', '') + '_created_id'
    sql += " %s INTEGER NOT NULL DEFAULT 0, " % (field)
    field = 'datetime_' + tbl.replace('customize.table_', '') + '_created_time'
    sql += " %s TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, " % (field)
    field = 'integer_' + tbl.replace('customize.table_', '') + '_updated_id'
    sql += " %s INTEGER NULL DEFAULT 0, " % (field)
    field = 'datetime_' + tbl.replace('customize.table_', '') + '_updated_time'
    sql += " %s TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP, " % (field)
    sql += " CONSTRAINT pk_%s PRIMARY KEY (%s) " % (colId, colId)
    sql += " ); "
    print(sql)

    return sql

def getProperties(key, sId):
    p = {}
    p['schema_id'] = sId
    p['properties_name'] = key
    idseq = {}
    idseq['idx'] = 0
    idseq['type'] = 'number'
    idseq['auth'] = {}
    idseq['auth']['edit'] = False
    idseq['auth']['view'] = False
    idseq['auth']['create'] = False
    idseq['auth']['search'] = True
    p['value'] = idseq
    return p

def getUis(key, sId, value):
    u = {}
    u['schema_id'] = sId
    u['properties_name'] = key
    u['value'] = value
    return u

def getLabels(key, sId, label):
    pln = {}
    pln['schema_id'] = sId
    pln['properties_name'] = key
    pln['object_label'] = label
    return pln

# def getSaveDatas(page, cId, uId):
#     if is_exist(page, 'page_key') == False:
#         return None

#     tbl = page['page_key']
#     idSeq = page['page_id_seq']
#     fs = page['form']
#     tbls = [ 'company.company_info', 'company.group_info', 'company.users_info', 'mente.page_info', 'system.api_info', 'system.server_info' ]
#     fix = False
#     if tbl in tbls:
#         istbl = tbl[(tbl.find('.')+1):]
#         fIdx = idSeq.find(tbl.split('.')[1]) + (len(tbl.split('.')[1]) + 1)
#         idSeq = idSeq[fIdx:]
#         fix = True
#     for f in fs:
#         schema = []
#         if isinstance(f['object'], list):
#             for obj in f['object']:
#                 fc = {}
#                 fc['object'] = obj
#                 schema.append(fc)
#         else:
#             schema.append(f)

#         cols = ""
#         vals = ""
#         for s in schema:
#             kp = s['object']['schema']['properties']
#             data = s['object']['data']
#             for key, value in kp.items():
#                 if is_exist(data, key) and key.find(istbl) != -1:
#                     ct = key[0:key.find('_')]
#                     col = key
#                     if fix:
#                         fIdx = col.find(tbl.split('.')[1]) + (len(tbl.split('.')[1]) + 1)
#                         col = key[fIdx:]
#                     cols += " %s," % (col)
#                     if ct in [ 'number', 'select', 'checkbox', 'radio' ]:
#                         vals += " %s," % (data[key])
#                     else:
#                         vals += " '%s'," % (data[key])
#     if cols.endswith(','):
#         cols = cols[0:len(cols)-1]
#     if vals.endswith(','):
#         vals = vals[0:len(vals)-1]
#     # print(cols)
#     # print(vals)
#     sql = " INSERT INTO %s(%s) VALUES(%s) RETURNING %s; " % (tbl, cols, vals, idSeq)
#     print(sql)
#     return " INSERT INTO %s(%s) VALUES(%s) RETURNING %s; " % (tbl, cols, vals, idSeq)