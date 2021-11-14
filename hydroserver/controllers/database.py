from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from hydroserver.model.model import Base

class DatabaseConnectionController(object):
    
    def __init__(self, sql_uri: str):
        """a simple class to create sessions and maintain connection information

        :param sql_uri: the connection string for the database
        :type sql_uri: str
        """
        #connect to database
        self._engine = create_engine(sql_uri)
        # initialize model in database (if not already done)
        Base.metadata.create_all(self._engine)
        self._session_maker = sessionmaker(bind=self._engine)
    
    def get_session(self) -> Session:
        """creates a session for the database

        :return: a newely created session for the database
        :rtype: Session
        """
        return self._session_maker()

