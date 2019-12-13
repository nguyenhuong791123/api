# -*- coding: UTF-8 -*-
import psycopg2
import sqlalchemy.pool as pool

def get_postgres_connection(conf):
    try:
        c = psycopg2.connect(host=conf.host, port=conf.port, database=conf.database, user=conf.user, password=conf.password)
    except psycopg2.Error as e:
        print(str(e))
        return None

    return c

def get_postgres_pool(conn, conf):
    return pool.QueuePool(conn, max_overflow=conf.max_overflow, pool_size=conf.pool_size)
