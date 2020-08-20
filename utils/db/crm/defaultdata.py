#-*- coding: UTF-8 -*-
import json
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

class DefaultData(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'default_data_info'

    properties_name = Column(String(30), primary_key=True)
    # properties_name = Column(String(30))
    value = Column(JSON)
    schema_id = Column(Integer, ForeignKey('mente.schema_info.schema_id'), primary_key=True)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<DefaultData %r>' % self.schema_id

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            setattr(self, key, o[key])

    def add(self, defData):
        try:
            self.db.session.add(defData)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, defDatas):
        try:
            self.db.session.add_all(defDatas)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

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
