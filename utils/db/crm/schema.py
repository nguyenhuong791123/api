#-*- coding: UTF-8 -*-
import json
import copy
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

from utils.cm.utils import is_exist, is_empty

class Schema(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'schema_info'

    schema_id = Column(Integer, primary_key=True, autoincrement=True)
    schema_type = Column(String(10), nullable=True)
    schema_key = Column(String(30))
    object_type = Column(String(10), nullable=True)
    idx = Column(Integer)

    form_id = Column(Integer, ForeignKey('mente.form_info.form_id'))

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Schema %r>' % self.schema_id

    def __json__(self, o, fId):
        for key in self.__mapper__.columns.keys():
            if key == 'schema_id':
                if (is_exist(o, key) == False or is_empty(o[key]) == True):
                    id = None
                else:
                    id = o[key]
                setattr(self, key, id)
            elif key == 'form_id':
                setattr(self, key, fId)
            elif key == 'object_type':
                setattr(self, key, o['type'])
            else:
                setattr(self, key, o[key])

    def get(self, fId):
        return self.db.session.query(Schema).filter(Schema.form_id==fId).all()

    def add(self, schema):
        try:
            self.db.session.add(schema)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, schemas):
        try:
            self.db.session.add_all(schemas)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, fId):
        try:
            self.db.session.query(Schema).filter(Schema.form_id==fId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class SchemaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Schema
        load_instance = True
        # fields = (
        #     'schema_id',
        #     'object_type',
        #     'object_key',
        #     'idx',
        #     'value',
        #     'page_id',
        # )
