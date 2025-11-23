from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from platformdirs import PlatformDirs
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from bushido.conf import DB_URL
from bushido.modules.orm import Base

APP_NAME = "bushido"
dirs = PlatformDirs(APP_NAME, appauthor=False)


def get_db_path() -> Path:
    state_dir = Path(dirs.user_state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir / "bushido.sqlite3"


class SessionFactory:
    def __init__(self, db_url: str = DB_URL) -> None:
        self._db_url = db_url
        self._engine = create_engine(db_url)
        self._sessionmaker = sessionmaker(bind=self._engine, expire_on_commit=False)

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def db_url(self) -> str:
        return self._db_url

    def init_db(self) -> None:
        Base.metadata.create_all(bind=self._engine)

    @contextmanager
    def session(self) -> Iterator[Session]:
        s = self._sessionmaker()
        try:
            yield s
        finally:
            s.close()

    @contextmanager
    def transaction(self) -> Iterator[Session]:
        s = self._sessionmaker()
        try:
            yield s
            s.commit()
        except Exception:
            s.rollback()
            raise
        finally:
            s.close()
