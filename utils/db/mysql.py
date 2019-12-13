

# -*- coding: UTF-8 -*-
import mysql
from ..cm.utils import is_empty

# def get_mysql_connection(conf):
#     try:
#         c = psycopg2.connect(host=conf.host, port=conf.port, database=conf.database, user=conf.user, password=conf.password)
#     except psycopg2.Error as e:
#         print(str(e))
#         return None

#     return c

def get_mysql_pool(conf):
    if is_empty(conf.pool_name):
        return None
    return mysql.connector.pooling.MySQLConnectionPool(pool_name=conf.pool_name, pool_size=conf.pool_size, **conf)

def mysql_select_execute(pool, query):
    return 'mysql'