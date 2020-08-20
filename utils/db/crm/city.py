#-*- coding: UTF-8 -*-
import json
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

class City(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'city_info'

    properties_name = Column(String(30), primary_key=True)
    value = Column(JSON)

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<City %r>' % self.code

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            setattr(self, key, o[key])

    def gets(self):
        return self.db.session.query(City).all()

    def add(self, c):
        try:
            self.db.session.add(c)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, cs):
        try:
            self.db.session.add_all(cs)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, code):
        try:
            self.db.session.query(City).filter(City.code==code).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class OptionPatitions(Options):
    @declared_attr
    def id(cls):
        return Column(Integer)

    @declared_attr
    def value(cls):
        return Column(String(30))

    @declared_attr
    def order(cls):
        return Column(Integer)

    def get_option_citys(self):
        return self.db.session.execute(text(getPatitions(cId, language)))

class CitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = City
        load_instance = True
