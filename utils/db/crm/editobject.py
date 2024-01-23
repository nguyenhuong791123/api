#-*- coding: UTF-8 -*-
import json
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

from utils.cm.utils import is_exist, is_empty, is_integer

class EditObject(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'edit_object_info'

    # edit_id = Column(Integer, primary_key=True, autoincrement=True)
    properties_name = Column(String(30), primary_key=True)
    edit_type = Column(Integer)
    value = Column(JSON)
    schema_id = Column(Integer, ForeignKey('mente.schema_info.schema_id'), primary_key=True)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<EditObject %r>' % (self.schema_id)

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            setattr(self, key, o[key])
            # if key == 'edit_id':
            #     if (is_exist(o, key) == False or is_empty(o[key]) == True):
            #         id = None
            #     else:
            #         id = o[key]
            #     setattr(self, key, id)
            # else:
            #     setattr(self, key, o[key])

    # def get(self, id):
    #     return self.db.session.query(EditObject).filter(EditObject.edit_id==id).one()

    def add(self, obj):
        try:
            # if is_integer(eObj['edit_id']) == True:
            #     obj = self.get(eObj['edit_id'])
            #     for key, value in eObj.items():
            #         setattr(obj, key, value)
            # else:
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

    # def update_all(self, eObjs):
    #     try:
    #         for o in eObjs:
    #             obj = self.get(o.edit_id)
    #             for key in obj.__mapper__.columns.keys():
    #                 setattr(obj, key, o[key])
    #         self.db.session.commit()
    #     except:
    #         self.db.session.rollback()
    #         raise

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
