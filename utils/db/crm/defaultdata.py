#-*- coding: UTF-8 -*-
import json
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

from utils.cm.utils import is_exist, is_empty, is_integer

class DefaultData(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'default_data_info'

    # data_id = Column(Integer, primary_key=True, autoincrement=True)
    properties_name = Column(String(30), primary_key=True)
    # properties_name = Column(String(30))
    value = Column(JSON)
    schema_id = Column(Integer, ForeignKey('mente.schema_info.schema_id'), primary_key=True)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<DefaultData %r>' % (self.schema_id)

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            setattr(self, key, o[key])
            # if key == 'data_id':
            #     if (is_exist(o, key) == False or is_empty(o[key]) == True):
            #         id = None
            #     else:
            #         id = o[key]
            #     setattr(self, key, id)
            # else:
            #     setattr(self, key, o[key])

    # def get(self, id):
    #     return self.db.session.query(DefaultData).filter(DefaultData.data_id==id).one()

    def add(self, obj):
        try:
            self.db.session.add(obj)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, objs):
        try:
            # if is_exist(objs[0], 'schema_id') and is_integer(objs[0]['schema_id']) == True:
            #     self.delete(objs[0]['schema_id'])
            self.db.session.add_all(objs)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    # def update_all(self, defDatas):
    #     try:
    #         for o in defDatas:
    #             obj = self.get(o.data_id)
    #             for key in obj.__mapper__.columns.keys():
    #                 setattr(obj, key, o[key])
    #         self.db.session.commit()
    #     except:
    #         self.db.session.rollback()
    #         raise

    def delete(self, sId):
        try:
            self.db.session.query(DefaultData).filter(DefaultData.schema_id==sId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class DefaultDataSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DefaultData
        load_instance = True
