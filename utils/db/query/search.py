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
    print(idSeq)
    cols = []
    gBy = []
    customize = False
    text = False
    if schema in [ 'company.company_info', 'company.group_info', 'company.users_info', 'system.api_info', 'system.server_info' ]:
        tbl = schema[(schema.find('.')+1):]
        print(idSeq)
        print(tbl)
        fIdx = (idSeq.find(tbl) + len(tbl)) + 1
        print(fIdx)
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
                if cn.startswith('text_'):
                    text = True
                # cn = c + ' AS ' + c
            columns[i] = None
    else:
        for i, c in enumerate(columns):
            cn = c
            if c.find('_seq_id_') > -1:
                cn = c[(c.find('_')+1):]
            cn = schema + '.' + cn + ' AS ' + c
            cols.append(cn)
            columns[i] = None

    columns = list(filter(None, columns))
    columns.extend(cols)

    sql = " SELECT json_agg(result) AS result FROM ("
    sql += " SELECT %s " % (",".join(columns))
    if customize:
        sql += " ,json_agg(json_build_object(ct.properties_name, ct.value)) AS items "
    sql += " FROM %s " % (schema)
    if reference is not None and len(reference) > 0:
        sql += " %s " % (reference)
    if where is not None and len(where) > 0:
        sql += " %s " % (where)
    if customize == True:
        sql += " LEFT JOIN mente.page_info p ON p.page_key='%s' " % (schema)
        if text:
            sql += " LEFT JOIN customize.text_field_datas ct ON ct.page_id=p.page_id AND ct.row_id=%s" % (idSeq)
        sql += " GROUP BY %s " % (",".join(gBy))
    sql += " ) AS result "
    print(sql)

    return sql
