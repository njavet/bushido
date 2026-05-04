import datetime
from collections.abc import Iterator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido.categories.db import SessionFactory
from bushido.categories.gym import GymUnit
from bushido.categories.lifting import LiftingSet, LiftingUnit
from bushido.categories.unit_service import UnitService


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
def service() -> UnitService:
    return UnitService()


def test_log_gym_unit_success(service: UnitService, session: Session) -> None:
    line = "weights 1800-1900 nautilus"
    service.log_unit(line, session)
    units = session.scalars(select(GymUnit)).all()
    assert len(units) == 1
    assert units[0].name == "weights"
    assert units[0].start_t == datetime.time(18, 0)
    assert units[0].end_t == datetime.time(19, 0)
    assert units[0].location == "nautilus"


def test_log_lifting_unit_success(service: UnitService, session: Session) -> None:
    line = "benchpress 100 5 180 100 5"
    service.log_unit(line, session)
    units = session.scalars(select(LiftingUnit)).all()
    assert len(units) == 1
    assert units[0].name == "benchpress"
    subs = session.scalars(select(LiftingSet)).all()
    assert len(subs) == 2
    assert subs[0].weight == 100
    assert subs[0].reps == 5
    assert subs[0].rest == 180
    assert subs[1].weight == 100
    assert subs[1].reps == 5
