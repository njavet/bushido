from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# project imports
from bushido.core.conf import DB_URL
from bushido.db.model.base import Base


class SessionFactory:
    def __init__(self, db_url=DB_URL):
        self._frozen = False
        self.db_url = db_url
        self._engine = create_engine(db_url)
        self._sessionmaker = sessionmaker(
            bind=self._engine, expire_on_commit=False
        )
        self._frozen = True

    @property
    def engine(self):
        return self._engine

    @property
    def db_url(self):
        return self._db_url

    @db_url.setter
    def db_url(self, db_url):
        if getattr(self, '_frozen', True):
            raise AttributeError('db_url is read only after init...')
        else:
            self._db_url = db_url

    def get_session(self):
        db = self._sessionmaker()
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def get_session_context(self):
        db = self._sessionmaker()
        try:
            yield db
        finally:
            db.close()

    def _setup_engine(self):
        engine = create_engine(self.db_url)
        Base.metadata.create_all(bind=engine)
        return engine

