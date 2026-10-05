from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from citadel.persistence import SessionFactory
from citadel.persistence.models import (
    Base,
)


@pytest.fixture(scope="session")
def session_factory() -> SessionFactory:
    sf = SessionFactory("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(sf.engine)
    return sf


@pytest.fixture
def session(session_factory: SessionFactory) -> Iterator[Session]:
    with session_factory.session() as s:
        try:
            yield s
        finally:
            s.close()
