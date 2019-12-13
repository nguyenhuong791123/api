# -*- coding: UTF-8 -*-
from types import MethodType

from ..cm.utils import is_empty, is_type, Obj

class E():
    MYSQL = 1
    POSTGRE = 2

class Q():
    SELECT = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4

class C():
    def __init__(self):
        self.engine = None
        self.engine_mode = E.MYSQL
        self.method = None
        self.query_mode = None
        self.result = None

    def add_engine(self, engine):
        if engine is not None:
            self.engine = engine

    def add_engine_mode(self, engine, emode):
        if engine is not None:
            self.engine = engine
        if emode is not None:
            self.engine_mode = emode

    def add_query(self, query):
        if is_empty(query) == False:
            self.query = query

    def add_fields(self, fields):
        for key in fields.keys():
            setattr(self, key, fields[key])

    def add_mode(self, qmode):
        if qmode is not None:
            self.query_mode = qmode

    def add_method(self, method):
        self.method = MethodType(method, self)

    def add_db_method_mode(self, qmode):
        self.query_mode = qmode
        self.method = MethodType(call_db_method, self)

    def is_check(self):
        if is_type(self.engine, Obj.QUEUEPOOL) == False:
            print('Connection engine to DB is required!!!')
            return False
        if is_type(self.method, Obj.METHOD) == False:
            print('Method is required!!!')
            return False
        return True

def call_db_method(self):
    if self.is_check() == False:
        return self.result

    if self.mode == Q.SELECT:
        # print('select')
        self.result = 'select'
    elif self.mode == Q.INSERT:
        # print('insert')
        self.result = 'insert'
    elif self.mode == Q.UPDATE:
        # print('update')
        self.result = 'update'
    elif self.mode == Q.DELETE:
        # print('delete')
        self.result = 'delete'
    else:
        # print('else')
        self.result = None

    print(self.__dict__)
    return self.result

# if __name__ == "__main__":
#     cls = C()
#     cls.add_fields({ 'a': None, 'b': '1' })
#     cls.add_db_method_mode(Q.SELECT)
#     print(cls.method())