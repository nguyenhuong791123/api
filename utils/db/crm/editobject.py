#-*- coding: UTF-8 -*-
import json
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

class EditObject(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'edit_object_info'

    properties_name = Column(String(30), primary_key=True)
    edit_type = Column(Integer)
    value = Column(JSON)
    schema_id = Column(Integer, ForeignKey('mente.schema_info.schema_id'), primary_key=True)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<EditObject %r>' % self.schema_id

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            setattr(self, key, o[key])

    def add(self, eObj):
        try:
            self.db.session.add(eObj)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, eObjs):
        try:
            self.db.session.add_all(eObjs)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, sId):
        try:
            self.db.session.query(EditObject).filter(EditObject.schema_id==sId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class EditObjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EditObject
        load_instance = True
