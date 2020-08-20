def createTablePatition(table):
    return " CREATE TABLE mente.%s PARTITION OF mente.option_info FOR VALUES IN ('%s') " % (table, table)

def dropTablePatition(table):
    return " DROP TABLE mente.%s " % (table)

def getDistinctPatitions(cId):
    return " SELECT json_agg(distinct option_name) AS patitions FROM mente.option_info WHERE company_id=%d " % (cId)

def getCitys():
    return " SELECT json_agg(json_build_object('value', code, 'label', name, 'order', code)) AS patitions FROM mente.city_info "

def getCompanys():
    return " SELECT json_agg(json_build_object('value', company_id, 'label', company_name, 'order', company_id)) AS patitions FROM company.company_info "

def getGroups():
    return " SELECT json_agg(json_build_object('value', group_id, 'label', group_name, 'order', group_id)) AS patitions FROM company.group_info "

def getUsers(gIds):
    sql = " SELECT json_agg(json_build_object('value', user_id, 'label', CONCAT(COALESCE(user_name_first, ''), ' ', COALESCE(user_name_last, '')), 'order', user_id)) AS patitions FROM company.users_info "
    if gIds is not None:
        sql += " WHERE group_id IN(%s) " % (",".join(gIds))
    return sql


def getPatitions(cId, language):
    sql = " SELECT json_agg(tbl) AS patitions FROM( "
    sql += " SELECT distinct "
    sql += " oi.option_name, "
    sql += " pl.object_label::jsonb->>'%s' as object_label " % (language)
    sql += " FROM mente.option_info oi "
    sql += " INNER JOIN mente.label_info pl ON pl.properties_name=oi.option_name "
    sql += " WHERE oi.company_id=%d " % (cId)
    sql += " ) AS tbl "
    return sql

def getOptionPatitions(cId, patitions):
    sql = " SELECT json_agg(tbl) AS patitions FROM( "
    sql += " SELECT "
    # sql += " SELECT json_build_object( "
    sql += " option_name, "
    sql += " json_agg(json_build_object('value', option_code, 'label', option_value, 'order', option_order)) AS options "
    sql += " FROM mente.option_info "
    sql += " WHERE company_id=%d " % (cId)
    if patitions is not None:
        sql += " AND option_name IN(%s) " % (",".join("'{0}'".format(e) for e in patitions))
    sql += " GROUP BY option_name "
    sql += " ) AS tbl "
    return sql
