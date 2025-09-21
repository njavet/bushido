from collections.abc import Generator, Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from bushido.core.conf import DB_URL
from bushido.db.model.base import Base


class SessionFactory:
    def __init__(self, db_url: str = DB_URL) -> None:
        self._frozen = False
        self.db_url = db_url
        self._engine = create_engine(db_url)
        self._sessionmaker = sessionmaker(
            bind=self._engine, expire_on_commit=False
        )
        self._frozen = True

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def db_url(self) -> str:
        return self._db_url

    @db_url.setter
    def db_url(self, db_url: str) -> None:
        if getattr(self, '_frozen', True):
            raise AttributeError('db_url is read only after init...')
        else:
            self._db_url = db_url

    def get_session(self) -> Generator[Session, None, None]:
        db = self._sessionmaker()
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def get_session_context(self) -> Iterator[Session]:
        db = self._sessionmaker()
        try:
            yield db
        finally:
            db.close()

    def _setup_engine(self) -> Engine:
        engine = create_engine(self.db_url)
        Base.metadata.create_all(bind=engine)
        return engine
