#-*- coding: UTF-8 -*-
import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
# from sqlalchemy.types  import *
# from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
from ..engine.db import Base

from utils.cm.utils import is_exist, is_empty
from ..query.page import getMenuQuery, getPageFields
from ..query.search import getColums

class Page(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'page_info'

    page_id = Column(Integer, primary_key=True, autoincrement=True)
    page_key = Column(String(45))
    page_flag = Column(Integer)
    page_order = Column(Integer)
    page_auth = Column(JSON)
    page_deleted = Column(Integer)
    updated_id = Column(Integer)
    updated_time = Column(DateTime)
    company_id = Column(Integer, ForeignKey('company.company_info.company_id'))

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Page %r>' % self.page_id

    def __json__(self, o, cId, uId):
        for key in self.__mapper__.columns.keys():
            if key in [ 'items', 'form', 'page_name' ]:
                continue
            elif key == 'page_id':
                if (is_exist(o, key) == False or is_empty(o[key]) == True):
                    id = None
                else:
                    id = o[key]
                setattr(self, key, id)
            elif key == 'page_auth':
                if (is_exist(o, key) == False or is_empty(o[key]) == True):
                    auth = None
                else:
                    auth = o[key]
                setattr(self, key, auth)
            elif is_exist(o, key) == False and key in [ 'page_flag', 'page_deleted' ]:
                setattr(self, key, 0)
            elif key == 'company_id':
                setattr(self, key, cId)
            elif key == 'updated_id':
                setattr(self, key, uId)
            elif key == 'updated_time':
                setattr(self, key, datetime.datetime.now())
            else:
                setattr(self, key, o[key])

    def gets(self, cId):
        try:
            return self.db.session.query(Page).filter(
                and_(Page.page_deleted==0, Page.company_id==cId)).all()
        except NoResultFound as ex:
            print(ex)
            return None

    def get(self, id):
        return self.db.session.query(Page).filter(and_(Page.page_id==id, Page.page_deleted==0)).one()

    def getIns(self, ids):
        return self.db.session.query(Page).filter(and_(Page.page_id.in_(ids), Page.page_deleted==0)).all()

    def get_max_order_by(self):
        return self.db.session.query(func.max(Page.page_order)).one()

    def add(self, page):
        try:
            self.db.session.add(page)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def add_all(self, pages):
        try:
            self.db.session.add_all(pages)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def update(self, page):
        try:
            p = self.get(page['page_id'])
            for key, value in page.items():
                setattr(p, key, value)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def update_all(self, items):
        try:
            ids = [p["page_id"] for p in items]
            pages = self.getIns(ids)
            for p in pages:
                for kp in items:
                    if kp['page_id'] != getattr(p, 'page_id'):
                        continue
                    else:
                        for key, value in kp.items():
                            if key == 'items':
                                continue
                            else:
                                setattr(p, key, value)
                        break

            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, pId):
        try:
            self.db.session.query(Page).filter(Page.page_id==pId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class PageMenu(Page):
    @declared_attr
    def items(cls):
        return Column(ARRAY([]))

    @declared_attr
    def page_name(cls):
        return Column(String(45))

    def get_menus(self, cId, language):
        return self.db.session.query(PageMenu).from_statement(text(getMenuQuery())).params(cId=cId, language=language).all()

    def get_colums(self, cId, pId, language):
        return self.db.session.query(PageMenu).from_statement(text(getColums())).params(cId=cId, pId=pId, language=language).all()

class PageForm(PageMenu):
    @declared_attr
    def form(cls):
        return Column(JSON([]))

    def get_form_fields(self, cId, pId, language):
        return self.db.session.query(PageForm).from_statement(text(getPageFields())).params(cId=cId, pId=pId, language=language).first()


class PageMenuSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Page
        load_instance = True
        fields = (
            'page_id',
            'page_name',
            'page_key',
            'page_flag',
            'page_auth',
            'page_order',
            'items',
        )

class PageFormSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Page
        load_instance = True
        fields = (
            'page_id',
            'page_name',
            'page_key',
            'page_auth',
            'form',
        )

class PageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Page
        load_instance = True
