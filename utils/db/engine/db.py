from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

Base = declarative_base()
class DB():
    from sqlalchemy.orm import sessionmaker
    global Session

    def __init__(self, *args):
        url = args[0]
        if str(url).startswith('mysql') == True:
            self.__table_args__ = None
            self.engine = create_engine('mysql+pymysql://' + url)
        else:
            self.__table_args__ = { 'schema': 'account' }
            self.engine = create_engine('postgresql+psycopg2://' + url)#connect_args={ "options": "-c statement_timeout=1" }

        Session = self.sessionmaker(bind=self.engine)
        self.session = Session()
        # Base.metadata.create_all(self.db.engine)

    def __repr__(self):
        return '<Engine(URL={url})>'.format(url=self.engine.url.__dict__)

    def close_session(self):
        if self.session.is_active == True:
            self.session.close()
            del self.session
        if self.engine is not None:
            self.engine.dispose()
            del self.engine
