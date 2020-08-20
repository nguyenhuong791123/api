#-*- coding: UTF-8 -*-
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy import and_

from ..engine.db import Base

class PageRel(Base):
    __table_args__ = { 'schema': 'mente' }
    __tablename__ = 'page_group_rel'

    page_id = Column(Integer, primary_key=True)
    page_group_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return '<PageRel %r>' % self.page_group_id

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __json__(self, pgId, pId):
        for key in self.__mapper__.columns.keys():
            if key == 'page_id':
                setattr(self, key, pId)
            elif key == 'page_group_id':
                setattr(self, key, pgId)
            else:
                setattr(self, key, o[key])

    def gets(self, pgId):
        return self.db.session.query(PageRel).filter(PageRel.page_group_id==pgId).all()

    def get(self, pId):
        return self.db.session.query(PageRel).filter(PageRel.page_id==pId).one()

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

    def delete(self, pId, group):
        try:
            if group == True:
                self.db.session.query(PageRel).filter(PageRel.page_group_id==pId).delete()
            else:
                self.db.session.query(PageRel).filter(PageRel.page_id==pId).delete()

            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class PageRelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PageRel
        load_instance = True
