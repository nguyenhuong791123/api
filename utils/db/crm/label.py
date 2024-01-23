#-*- coding: UTF-8 -*-
import json
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

from utils.cm.utils import is_exist, is_empty, is_integer

class Label(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'label_info'

    properties_name = Column(String(30), primary_key=True)
    object_label = Column(JSON)
    schema_id = Column(Integer)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Label %r>' % self.properties_name

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            setattr(self, key, o[key])

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

    def delete_page_id(self, pId):
        try:
            self.db.session.query(Label).filter(and_(Label.schema_id==pId, Label.properties_name==str(pId))).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, sId):
        try:
            self.db.session.query(Label).filter(Label.schema_id==sId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete_in_properties_name(self, names):
        try:
            self.db.session.query(Label).filter(Label.properties_name.in_(names)).delete(synchronize_session='fetch')
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class LabelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Label
        load_instance = True
