#-*- coding: UTF-8 -*-
import json
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

from utils.cm.utils import is_exist, is_empty, is_integer

class Ui(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'ui_info'

    properties_name = Column(String(30), primary_key=True)
    value = Column(JSON)
    schema_id = Column(Integer, ForeignKey('mente.schema_info.schema_id'), primary_key=True)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Ui %r>' % (self.schema_id)

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            setattr(self, key, o[key])

    def add_all(self, objs):
        try:
            self.db.session.add_all(objs)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, sId):
        try:
            self.db.session.query(Ui).filter(Ui.schema_id==sId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class UiSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ui
        load_instance = True
