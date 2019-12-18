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
    rePool = pool.QueuePool(conn, max_overflow=conf.max_overflow, pool_size=conf.pool_size)
    if rePool:
        print("Connection pool created successfully!!!")
    return rePool

def postgre_select_execute(inPool, query):
    conn = inPool.connect()
    if(conn):
        print("Successfully recived connection from connection pool!!!")
    print(query)
    try:
        cur = conn.cursor()
        print(query)
        cur.execute(query)
        rec = cur.fetchall()
        for row in rec:
            print (row)

        cur.close()
    except Exception as ex:
        print(ex)
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if (inPool):
            inPool.closeall
        print("PostgreSQL connection pool is closed")