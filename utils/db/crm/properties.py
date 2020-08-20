#-*- coding: UTF-8 -*-
import json
import copy
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

from utils.cm.utils import *

class Properties(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'properties_info'

    properties_id = Column(Integer, primary_key=True, autoincrement=True)
    properties_name = Column(String(30), primary_key=True)
    # properties_name = Column(String(30))
    value = Column(JSON)
    schema_id = Column(Integer, ForeignKey('mente.schema_info.schema_id'), primary_key=True)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Properties %r>' % self.schema_id

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            if key == 'properties_id':
                if (is_exist(o, key) == False or is_empty(o[key]) == True):
                    id = None
                else:
                    id = o[key]
                setattr(self, key, id)
            elif key == 'value':
                value = copy.copy(o[key])
                del value['obj']
                if is_exist(value, 'options') == True:
                    del value['options']
                setattr(self, key, value)
            else:
                setattr(self, key, o[key])

    def add(self, propertie):
        try:
            self.db.session.add(propertie)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, properties):
        try:
            self.db.session.add_all(properties)
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
