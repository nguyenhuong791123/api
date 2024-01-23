#-*- coding: UTF-8 -*-
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy import and_

from utils.cm.utils import is_exist, is_empty, is_integer
from ..engine.db import Base

class Server(Base):
    __table_args__ = { 'schema': 'system' }
    __tablename__ = 'server_info'

    server_id = Column(Integer, primary_key=True, autoincrement=True)
    server_name = Column(String(45))
    server_type = Column(Integer)
    host = Column(String(100))
    port = Column(Integer)
    database = Column(String(20))
    username = Column(String(15))
    password = Column(String(70))
    company_id = Column(Integer, ForeignKey('company.company_info.company_id'))

    def __repr__(self):
        return '<Server %r>' % self.server_id

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __json__(self, o, cId, uId):
        for key in self.__mapper__.columns.keys():
            if key == 'server_id':
                if (is_exist(o, key) == False or is_empty(str(o[key])) == True):
                    id = None
                else:
                    id = o[key]
                setattr(self, key, id)
            elif key == 'page_group_id':
                setattr(self, key, pgId)
            else:
                setattr(self, key, o[key])

    def add(self, obj):
        try:
            self.db.session.add(obj)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

    def delete(self, sId):
        try:
            self.db.session.query(PageRel).filter(Server.server_id==sId).delete()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            raise

class Serverchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Server
        load_instance = True
