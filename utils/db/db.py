# -*- coding: UTF-8 -*-
from ..cm.utils import is_exist
from .engine.postgre import *
from .engine.mysql import *

class E():
    MYSQL = 1
    POSTGRE = 2

class Q():
    SELECT = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4

class Config():
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.database = kwargs['database']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.max_overflow = 10
        self.pool_size = 5
        self.pool_name = None
        self.charset = 'utf8mb4'

    def set_port(self, port):
        if port is not None and port > 0:
            self.port = port

    def set_charset(self, charset):
        if charset is not None:
            self.charset = charset

    def set_max_overflow(overflow):
        if overflow is not None and overflow > 0:
            self.max_overflow = overflow

    def set_pool_size(poolsize):
        if poolsize is not None and poolsize > 0:
            self.pool_size = poolsize

    def set_pool_name(self, poolname):
        if poolname is not None:
            self.pool_name = poolname

    def get_uri(self):
        if self.port is not None:
            return 'postgresql+psycopg2://' + self.username + ':' + self.password + '@' + self.host + ':' + str(self.port) + '/' + self.database
        else:
            return 'postgresql+psycopg2://' + self.username + ':' + self.password + '@' + self.host + '/' + self.database

def get_engine(auth):
    if is_exist(auth, 'engine_mode') == False:
        return None

    emode = auth['engine_mode']
    if emode == E.POSTGRE:
        return get_postgres_engine(auth)
    elif emode == E.MYSQL:
        return get_mysql_engine(auth)
    else:
        return None

def get_postgres_engine(auth):
    conf = Config(host=auth['host'], database=auth['database'], username=auth['username'], password=auth['password'])
    conf.set_port(auth['port'])
    conn = get_postgres_connection(conf)
    return get_postgres_pool(conn, conf)

def get_mysql_engine(auth):
    conf = Config(host=auth['host'], database=auth['database'], username=auth['username'], password=auth['password'])
    # conf.set_port(3306) # Default Port 3306
    conf.set_pool_name('scapp_pool')
    return get_mysql_pool(conf)
