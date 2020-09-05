#-*- coding: UTF-8 -*-
import json
import copy
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

from utils.cm.utils import is_exist, is_empty, is_integer

class Properties(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'properties_info'

    properties_id = Column(Integer, primary_key=True, autoincrement=True)
    properties_name = Column(String(30), primary_key=True)
    value = Column(JSON)
    schema_id = Column(Integer, ForeignKey('mente.schema_info.schema_id'), primary_key=True)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Properties %r %r>' % (self.schema_id, self.properties_id)

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            if key == 'properties_id':
                if (is_exist(o, key) == False or is_integer(o[key]) == False):
                    id = None
                else:
                    id = o[key]
                setattr(self, key, id)
            elif key == 'value':
                value = copy.copy(o[key])
                if is_exist(value, 'obj') == True:
                    del value['obj']
                if is_exist(value, 'options') == True:
                    del value['options']
                if is_exist(value, 'obj_label') == True:
                    del value['obj_label']
                setattr(self, key, value)
            else:
                setattr(self, key, o[key])

    def get_by_schema_id(self, sId):
        return self.db.session.query(Properties).filter(Properties.schema_id==sId).all()

    def add(self, obj):
        try:
            self.db.session.add(obj)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, objs):
        try:
            self.db.session.add_all(objs)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, sId):
        try:
            self.db.session.query(Properties).filter(Properties.schema_id==sId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class PropertiesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Properties
        load_instance = True
