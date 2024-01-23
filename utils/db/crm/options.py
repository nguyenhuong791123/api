#-*- coding: UTF-8 -*-
import json
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
from ..engine.db import Base

from utils.cm.utils import is_exist, is_empty
from ..query.options import *

class Options(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'option_info'

    option_id = Column(Integer, primary_key=True, autoincrement=True)
    option_name = Column(String(50), nullable=True)
    option_code = Column(String(20))
    option_value = Column(String(70), nullable=True)
    option_order = Column(Integer)
    company_id = Column(Integer, ForeignKey('company.company_info.company_id'))

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Options %r>' % self.option_id

    def __json__(self, o):
        for key in self.__mapper__.columns.keys():
            if key == 'option_id':
                if (is_exist(o, key) == False or is_empty(o[key]) == True):
                    id = None
                else:
                    id = o[key]
                setattr(self, key, id)
            else:
                setattr(self, key, o[key])

    def add_patition(self, table):
        try:
            self.db.session.execute(text(createTablePatition(table)))
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def drop_patition(self, table):
        try:
            self.db.session.execute(text(dropTablePatition(table)))
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def get_options_by_patition(self, cId, patition):
        return self.db.session.query(Options).filter(
            and_(Options.company_id==cId, Options.option_name==patition)).all()

    def get_options_by_patitions(self, cId, patitions):
        return self.db.session.query(Options).filter(
            and_(Options.company_id==cId, Options.option_name.in_(patitions))).all()

    def add(self, opt):
        try:
            self.db.session.add(opt)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, opts):
        try:
            self.db.session.add_all(opts)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete_name(self, name):
        try:
            self.db.session.query(Options).filter(Options.option_name==name).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, oId):
        try:
            self.db.session.query(Options).filter(Options.option_id==oId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class OptionPatitions(Options):
    @declared_attr
    def patitions(cls):
        return Column(JSON([]))

    def get_patitions(self, cId, language):
        return self.db.session.execute(text(getPatitions(cId, language)))

    def get_option_patitions(self, cId, patitions):
        return self.db.session.execute(text(getOptionPatitions(cId, patitions)))

    def get_distinct_patitions(self, cId):
        return self.db.session.execute(text(getDistinctPatitions(cId)))

    def get_option_citys(self):
        return self.db.session.execute(text(getCitys()))

    def get_option_companys(self):
        return self.db.session.execute(text(getCompanys()))

    def get_option_groups(self):
        return self.db.session.execute(text(getGroups()))

    def get_option_users(self, gIds):
        return self.db.session.execute(text(getUsers(gIds)))


class OptionsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Options
        load_instance = True

class OptionPatitionsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Options
        load_instance = True
        fields = (
            'patitions',
        )
