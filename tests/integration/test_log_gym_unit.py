import datetime
from collections.abc import Iterator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido.core.result import Ok
from bushido.infra.db import SessionFactory
from bushido.modules.dtypes import ParsedUnit
from bushido.modules.factory import Factory
from bushido.modules.gym import GymUnit
from bushido.service.log_unit import LogUnitService


@pytest.fixture(scope="session")
def session_factory() -> SessionFactory:
    sf = SessionFactory("sqlite+pysqlite:///:memory:")
    sf.init_db()
    return sf


@pytest.fixture
def session(session_factory: SessionFactory) -> Iterator[Session]:
    with session_factory.session() as s:
        try:
            yield s
        finally:
            s.close()


@pytest.fixture
def service() -> LogUnitService:
    return LogUnitService(factory=Factory())


def test_log_gym_unit_success(service: LogUnitService, session: Session) -> None:
    line = "weights 1800-1900 nautilus"
    res = service.log_unit(line, session)
    assert isinstance(res, Ok)
    assert isinstance(res.value, ParsedUnit)
    units = session.scalars(select(GymUnit)).all()
    assert len(units) == 1
    assert units[0].name == "weights"
    assert units[0].start_t == datetime.time(18, 0)
    assert units[0].end_t == datetime.time(19, 0)
    assert units[0].location == "nautilus"
