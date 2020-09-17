def getColums():
    sql = " SELECT p.page_id, p.page_key, p.page_auth::jsonb, l.object_label::jsonb->>:language AS page_name, json_agg(f.fields) AS items FROM ( "
    sql += " SELECT f.page_id, "
    sql += " json_build_object( "
    sql += " 'field', p.properties_name, "
    sql += " 'search', p.value::jsonb->'auth'->'search', "
    sql += " 'label', pl.object_label::jsonb->>:language, "
    sql += " 'type', substring(p.properties_name, 0, position('_' IN p.properties_name)) "
    sql += " ) AS fields "
    sql += " FROM mente.form_info f "
    sql += " LEFT JOIN mente.schema_info s ON f.form_id=s.form_id "
    sql += " INNER JOIN mente.properties_info p ON p.schema_id=s.schema_id "
    sql += " INNER JOIN mente.label_info pl ON pl.properties_name=p.properties_name AND pl.schema_id=p.schema_id AND p.schema_id=s.schema_id "
    sql += " ) AS f "
    sql += " INNER JOIN mente.page_info p ON p.page_id=f.page_id "
    sql += " INNER JOIN mente.label_info l ON l.properties_name=p.page_id::varchar AND l.schema_id=p.page_id "
    sql += " WHERE p.company_id=:cId AND p.page_deleted=0 AND p.page_id=:pId "
    sql += " GROUP BY p.page_id, l.object_label "
    return sql

def getDatas(schema, columns, idSeq, where, reference):
    print(columns)
    print(where)
    cols = []
    gBy = []
    customize = False
    text = False
    varchar = False
    joins = []
    if schema in [ 'company.company_info', 'company.group_info', 'company.users_info', 'system.api_info', 'system.server_info' ]:
        tbl = schema[(schema.find('.')+1):]
        fIdx = (idSeq.find(tbl) + len(tbl)) + 1
        idSeq = schema + '.' + idSeq[fIdx:]
        for i, c in enumerate(columns):
            if c.find(tbl) > -1:
                cn = c[(c.find('_')+1):].replace(tbl + '_', '')
                cn = schema + '.' + cn
                col = cn + ' AS ' + c
                gBy.append(cn)
                cols.append(col)
            else:
                cn = c
                customize = True
                ct = c[0:c.find('_')]
                # print(ct)
                if ct == 'text':
                    ct = 'varchar'
                elif ct == 'month':
                    ct = 'date'
                elif ct in [ 'textarea', 'editor' ]:
                    ct = 'text'
                elif ct in [ 'file', 'image']:
                        ct = 'file'
                elif ct in [ 'number', 'checkbox', 'radio', 'select' ]:
                    if ct == 'number':
                        ct = 'double'
                    else:
                        ct = 'integer'
                if ct not in joins:
                    joins.append(ct)
            columns[i] = None
    else:
        for i, c in enumerate(columns):
            cn = c
            if c.find('_seq_id_') > -1:
                idSeq = schema + '.' + idSeq[(idSeq.find('_')+1):]
                cn = c[(c.find('_')+1):]
            if c.endswith('_customize'):
                customize = True
                ct = c[0:c.find('_')]
                if ct == 'text':
                    ct = 'varchar'
                elif ct == 'month':
                    ct = 'date'
                elif ct in [ 'textarea', 'editor']:
                    ct = 'text'
                elif ct in [ 'file', 'image']:
                    ct = 'file'
                elif ct in [ 'number', 'checkbox', 'radio', 'select' ]:
                    if ct == 'number':
                        ct = 'double'
                    else:
                        ct = 'integer'
                if ct not in joins:
                    joins.append(ct)
            else:
                col = schema + '.' + cn + ' AS ' + c
                gBy.append(cn)
                cols.append(col)
            columns[i] = None

    columns = list(filter(None, columns))
    columns.extend(cols)

    sql = " SELECT json_agg(result) AS result FROM ("
    sql += " SELECT %s " % (",".join(columns))
    if customize == True and (len(joins) > 0) and idSeq is not None:
        for i, j in enumerate(joins):
            if i == 0:
                sql += " ,json_agg(json_build_object('field_id', %s.field_id, COALESCE(%s.properties_name, ''), %s.value))::jsonb " % (j, j, j)
            else:
                sql += " || json_agg(json_build_object('field_id', %s.field_id, COALESCE(%s.properties_name, ''), %s.value))::jsonb " % (j, j, j)
        sql += " AS items "
    sql += " FROM %s " % (schema)

    if customize == True and (len(joins) > 0) and idSeq is not None:
        # print(joins)
        sql += " LEFT JOIN mente.page_info p ON p.page_key='%s' " % (schema)
        for join in joins:
            sql += " LEFT JOIN customize.%s_field_datas %s ON %s.page_id=p.page_id AND %s.row_id=%s" % (join, join, join, join, idSeq)
    if reference is not None and len(reference) > 0:
        sql += " %s " % (reference)
    if where is not None and len(where) > 0:
        sw = where[(where.find('_')+1):]
        if schema in [ 'company.company_info', 'company.group_info', 'company.users_info', 'system.api_info', 'system.server_info' ]:
            s1st = sw.find('_') + 1
            wTbl = sw[0:sw.find('_', s1st)]
            sw = sw.replace(wTbl + '_', wTbl + '.')
        sql += " WHERE %s " % (sw)

    if customize == True and (len(joins) > 0) and idSeq is not None:
        sql += " GROUP BY %s " % (",".join(gBy))
    sql += " ) AS result "
    print(sql)

    return sql
