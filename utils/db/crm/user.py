#-*- coding: UTF-8 -*-
from passlib.hash import sha256_crypt
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base

class User(Base):
    __table_args__ = { 'schema': 'company' }
    __tablename__ = 'users_info'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_code = Column(String(30), nullable=True)
    user_login_id = Column(String(8), nullable=True)
    user_password = Column(String(70), nullable=True)
    user_name_first = Column(String(70), nullable=True)
    user_name_last = Column(String(70), nullable=True)
    user_kana_first = Column(String(70), nullable=True)
    user_kana_last = Column(String(70), nullable=True)
    user_post = Column(String(8))
    user_city = Column(Integer)
    user_address = Column(String(150))
    user_address_kana = Column(String(200))
    user_image = Column(Text)
    user_mail = Column(String(150))
    user_firewall = Column(Integer)
    user_global_flag = Column(Integer)
    user_manager = Column(Integer)
    user_cti_flag = Column(Integer)
    user_theme = Column(String(15))
    user_memo = Column(String(500))
    user_order = Column(Integer)
    user_view_menu = Column(Integer)
    user_deleted = Column(Integer)
    created_id = Column(Integer)
    created_time = Column(DateTime)
    updated_id = Column(Integer)
    updated_time = Column(DateTime)
    group_id = Column(Integer, ForeignKey('company.group_info.group_id'))

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<User %r>' % self.user_id

    def gets(self, cId):
        return self.db.session.query(User).filter(
            and_(User.group_id==Group.group_id, User.user_deleted==0, Group.company_id==cId)).all()

    def get(self, id):
        return self.db.session.query(User).filter(and_(User.user_deleted==0, User.user_id==id)).one()

    def get_login(self, uId, uPw):
        result = self.db.session.query(User).filter(
            and_(User.user_deleted==0, User.user_login_id==uId)).first()
        if result is not None:
            verify = sha256_crypt.verify(uPw, '$5$rounds=10000' + result.user_password)
            if verify == True:
                return result
            return None
        return None

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = (
                'user_id',
                'group_id',
                'user_address',
                'user_address_kana',
                'user_city',
                'user_code',
                'user_firewall',
                'user_global_flag',
                'user_cti_flag',
                'user_image',
                'user_kana_first',
                'user_kana_last',
                'user_login_id',
                'user_mail',
                'user_manager',
                'user_memo',
                'user_name_first',
                'user_name_last',
                'user_order',
                'user_post',
                'user_theme',
                'user_view_menu',
                'created_id',
                'created_time',
                'updated_id',
                'updated_time',
            )
