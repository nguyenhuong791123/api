#-*- coding: UTF-8 -*-
from passlib.hash import sha256_crypt
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base
from .group import Group

class Company(Base):
    __table_args__ = { 'schema': 'company' }
    __tablename__ = 'company_info'
    company_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(45), nullable=True)
    company_post = Column(String(8))
    company_city = Column(Integer)
    company_address = Column(String(150))
    company_address_kana = Column(String(200))
    company_logo = Column(Text)
    company_home_page = Column(String(150))
    company_copy_right = Column(String(150))
    company_global_ip = Column(String(120))
    company_cti_flag = Column(Integer)
    company_memo = Column(String(500))
    company_global_locale = Column(Integer)
    company_theme = Column(String(15))
    company_use_system_auth = Column(Integer)
    company_use_api = Column(Integer)
    company_start_use_date = Column(DateTime)
    company_basic_login_id = Column(String(30))
    company_basic_password = Column(String(70))
    company_deleted = Column(Integer)
    updated_id = Column(Integer)
    updated_time = Column(DateTime)
    groups = relationship("Group")

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Company %r>' % self.company_id

    def gets(self):
        return self.db.session.query(Company).all()

    def get(self, id):
        return self.db.session.query(Company).filter(Company.company_id==id).first()

    def get_basic(self, id, pw):
        if id is None or pw is None:
            return None
        # newH = sha256_crypt.using(rounds=10000).hash(pw)
        # print(newH)
        # print(sha256_crypt.verify(pw, '$5$rounds=10000$BdgUHFSOc1D4nONw$qhmq23aKTI9PBqZsXFJqqsqPDUsUf0zuwseCO1ArnO0'))
        result = self.db.session.query(Company).filter(
            and_(Company.company_deleted==0, Company.company_basic_login_id==id)).first()
        if result is not None:
            verify = sha256_crypt.verify(pw, '$5$rounds=10000' + result.company_basic_password)
            if verify == True:
                return result
            return None
        return None

class CompanyBasic(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True
        fields = ('company_id',)

class CompanyMode(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True
        fields = (
            'company_id',
            'company_name',
            'company_logo',
            'company_theme',
            'company_global_locale',
            'company_cti_flag',
            'company_use_api',
            'company_copy_right',
            'company_home_page',)

class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
