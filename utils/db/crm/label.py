#-*- coding: UTF-8 -*-
import json
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

class Label(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'label_info'

    properties_name = Column(String(30), primary_key=True)
    object_label = Column(JSON)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Label %r>' % self.properties_name

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            setattr(self, key, o[key])

    def add(self, label):
        try:
            self.db.session.add(label)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, name):
        try:
            self.db.session.query(Label).filter(Label.properties_name==name).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class LabelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Label
        load_instance = True
