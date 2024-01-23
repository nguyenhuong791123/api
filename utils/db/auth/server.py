#-*- coding: UTF-8 -*-
from passlib.hash import sha256_crypt
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base
from ..crm.company import Company

class Server(Base):
    __table_args__ = { 'schema': 'system' }
    __tablename__ = 'server_info'
    server_id = Column(Integer, primary_key=True, autoincrement=True)
    server_name = Column(String(45), nullable=True)
    server_type = Column(Integer)
    host = Column(String(100))
    port = Column(Integer)
    database = Column(String(20))
    username = Column(String(15))
    password = Column(String(70))
    company_id = Column(Integer, ForeignKey('company.company_info.company_id'))
    company = relationship("Company")

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        # Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Server %r>' % self.server_id

    def gets(self, cId):
        return self.db.session.query(Server).filter(
            and_(Server.company_id==Company.company_id, Company.company_deleted==0, Company.company_id==cId)).all()

    def get(self, id):
        return self.db.session.query(Server).filter(Server.server_id==id).first()

    def get_server_by_type(self, cId, type):
        if cId is None or type is None:
            return None
        result = self.db.session.query(Server).filter(
            and_(Server.company_id==Company.company_id, Server.server_type==type, Company.company_deleted==0, Company.company_id==cId)).first()
        if result is None:
            return None
        return result

    def close_session(self):
        if self.db.session.is_active == True:
            self.db.session.close()
            del self.db.session
        if self.db.engine is not None:
            self.db.engine.dispose()
            del self.db.engine

class ServerInfo(SQLAlchemyAutoSchema):
    class Meta:
        model = Server
        fields = (
                'host',
                'port',
                'database',
                'username',
                'password',
            )

class ServerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Server
