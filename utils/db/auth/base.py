# -*- coding: UTF-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

from utils.cm.utils import is_empty 
from utils.db.db import Config

# postgresqlのDBの設定
DATABASE = "postgresql://postgres:postgres080@sc-p-db:5432/scapp"

# Engineの作成
ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    # TrueにするとSQLが実行される度に出力される
    echo=True
)

# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するなど。
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()

# class Base():
#     def __init__(self):
#         self.engine = None
#         self.session = None
#         self.base = None

#     def set_engine(self, auth):
#         self.engine = postgres_engine(auth)

#     def set_session(self):
#         self.session = postgres_session(self.engine)

#     def set_base(self):
#         self.base = postgres_base(self.session)

#     def create_all(self):
#         self.base.metadata.create_all(bind=self.engine)

# def postgres_engine(auth):
#     conf = Config(host=auth['host'], database=auth['database'], username=auth['username'], password=auth['password'])
#     # uri = "postgresql://postgres:@192.168.1.19:5432/flask_tutorial"
#     conf.set_port(auth['port'])
#     conf.set_charset('utf-8')
#     uri = conf.get_uri()
#     return create_engine(uri, encoding=conf.charset, echo=True)

# def postgres_session(engine):
#     return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# def postgres_base(session):
#     mode = declarative_base()
#     mode.query = session.query_property()
#     return mode