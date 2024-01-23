#-*- coding: UTF-8 -*-
import json
import copy
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

from utils.cm.utils import is_exist, is_empty, is_integer

class Form(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'form_info'

    form_id = Column(Integer, primary_key=True, autoincrement=True)
    object_type = Column(String(10), nullable=True)
    object_key = Column(String(50))
    class_name = Column(String(50))
    idx = Column(Integer)

    page_id = Column(Integer, ForeignKey('mente.page_info.page_id'))

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Form %r %r>' % (self.page_id, self.form_id)

    def __json__(self, o, pId):
        for key in self.__mapper__.columns.keys():
            if key == 'form_id':
                if (is_exist(o, key) == False or is_empty(o[key]) == True):
                    id = None
                else:
                    id = o[key]
                setattr(self, key, id)
            elif key == 'page_id':
                setattr(self, key, pId)
            elif key == 'class_name':
                setattr(self, key, o['className'])
            else:
                setattr(self, key, o[key])

    def get(self, id):
        return self.db.session.query(Form).filter(Form.form_id==id).first()

    def get_by_page_id(self, pId):
        return self.db.session.query(Form).filter(Form.page_id==pId).all()

    def add(self, form):
        try:
            self.db.session.add(form)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, fos):
        try:
            self.db.session.add_all(fos)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def update(self, form):
        try:
            obj = self.get(form['form_id'])
            for key in obj.__mapper__.columns.keys():
                if is_exist(form, key) == True or key == 'class_name':
                    if key == 'class_name':
                        setattr(obj, key, form['className'])
                    else:
                        setattr(obj, key, form[key])
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, pId):
        try:
            self.db.session.query(Form).filter(Form.page_id==pId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class FormSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Form
        load_instance = True

