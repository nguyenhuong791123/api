# -*- coding: UTF-8 -*-
from types import MethodType

from ..cm.utils import is_empty, is_type, Obj
from .db import E, Q, get_engine
from .postgre import postgre_select_execute
from .mysql import mysql_select_execute

class C():
    def __init__(self):
        self.info = None
        # self.engine = None
        self.engine_mode = E.MYSQL
        self.method = None
        self.query_mode = None
        self.query = None
        self.result = None

    def add_info(self, info):
        if info is not None:
            self.info = info

    # def add_engine(self, engine):
    #     if engine is not None:
    #         self.engine = engine

    # def add_engine_mode(self, engine, emode):
    #     if engine is not None:
    #         self.engine = engine
    #     if emode is not None:
    #         self.engine_mode = emode

    def add_engine_mode(self, emode):
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
        if is_type(self.method, Obj.METHOD) == False:
            print('Method is required!!!')
            return False
        return True

def call_db_method(self):
    if self.is_check() == False:
        return self.result

    engine = get_engine(self.info)
    print(engine.__dict__)
    if self.query_mode == Q.SELECT:
        if self.engine_mode == E.POSTGRE:
            postgre_select_execute(engine, self.query)
        elif self.engine_mode == E.MYSQL:
            mysql_select_execute(engine, self.query)
        else:
            self.result = None
    elif self.query_mode == Q.INSERT:
        # print('insert')
        self.result = 'insert'
    elif self.query_mode == Q.UPDATE:
        # print('update')
        self.result = 'update'
    elif self.query_mode == Q.DELETE:
        # print('delete')
        self.result = 'delete'
    else:
        # print('else')
        self.result = None

    print(self.__dict__)
    return self.result
