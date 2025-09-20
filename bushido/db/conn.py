from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# project imports
from bushido.core.conf import DB_URL


class SessionFactory:
    def __init__(self, db_url=DB_URL):
        self._fronzen = False
        self.db_url = db_url
        self._engine = create_engine(db_url)
        self._sessionmaker = sessionmaker(
            bind=self._engine, expire_on_commit=False
        )
        self._fronzen = True

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
