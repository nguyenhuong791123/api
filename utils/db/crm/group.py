#-*- coding: UTF-8 -*-
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.types  import *
from sqlalchemy.orm import *
from ..engine.db import Base
from .user import User

class Group(Base):
    __table_args__ = { 'schema': 'company' }
    __tablename__ = 'group_info'
    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(45), nullable=True)
    group_code = Column(String(45), nullable=True)
    group_parent_id = Column(Integer)
    group_tree_id = Column(String(500))
    group_order = Column(Integer)
    group_memo = Column(String(500))
    group_deleted = Column(Integer)
    updated_id = Column(Integer)
    updated_time = Column(DateTime)
    company_id = Column(Integer, ForeignKey('company.company_info.company_id'))
    users = relationship("User")

    def __init__(self, *args):
        engine = args[0]
        self.db = engine
        Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Group %r>' % self.group_id

    def gets(self, cId):
        return self.db.session.query(Group).filter(
            and_(Group.group_deleted==0, Group.company_id==Company.company_id, Company.company_id==cId)).all()

    def get(self, id):
        return self.db.session.query(Group).filter(Group.group_id==id).first()

class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        fields = (
                'group_id',
                'group_name',
                'group_code',
                'group_parent_id',
                'group_order',
                'group_memo',
                'company_id',
                'updated_id',
                'updated_time',
                'users',
            )