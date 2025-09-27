from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from bushido.core.conf import DB_URL
from bushido.infra.db.model.base import Base


class SessionFactory:
    def __init__(self, db_url: str = DB_URL, create_schema: bool = False) -> None:
        self._db_url = db_url
        self._engine = create_engine(db_url)
        if create_schema:
            Base.metadata.create_all(bind=self._engine)

        self._sessionmaker = sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def db_url(self) -> str:
        return self._db_url

    @contextmanager
    def session(self) -> Iterator[Session]:
        s = self._sessionmaker()
        try:
            yield s
            s.commit()
        except Exception:
            s.rollback()
            raise
        finally:
            s.close()

