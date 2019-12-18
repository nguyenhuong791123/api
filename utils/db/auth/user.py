#-*- coding: UTF-8 -*-
from sqlalchemy import and_

from utils.cm.bcrypts import Bcrypt
from .db import db, ma

class User(db.Model):
    __tablename__ = 'auth_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def get_user_list():
        users = db.session.query(User).all()

        if users is None:
            return []

        return users

    def is_exist(user):
        crypt = Bcrypt()
        crypt.set_salt()
        pw = crypt.get_hashpw(user['password'])
        result = db.session.query(User).filter(User.email==user['email']).all()
        # result = db.session.query(User).filter(
        #     and_(User.email==user['email'], User.password==pw)).limit(1).all()
        if result is None:
            return False
        
        crypt = Bcrypt()
        crypt.set_salt()
        auth = result[0]
        return crypt.get_checkpw(user['password'], auth.password)
        # return (user is not None and len(user) > 0)

    def regist_user(user):
        crypt = Bcrypt()
        crypt.set_salt()
        pw = crypt.get_hashpw(user['password'])
        db.session.add(User(email=user['email'], password=pw))
        db.session.commit()

        del user['password']
        return user

class UserSchema(ma.ModelSchema):
    class Meta:
      model = User
    #   fields = ('id', 'email', 'password')
      fields = ('id', 'email')
