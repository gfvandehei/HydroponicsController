from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from hydroserver.model.model import Base

class DatabaseConnectionController(object):

    def __init__(self, sql_uri: str):
        self._engine = create_engine(sql_uri)
        Base.metadata.create_all(self._engine)
        self._session_maker = sessionmaker(bind=self._engine)
    
    def get_session(self) -> Session:
        return self._session_maker()

