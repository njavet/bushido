from collections.abc import Iterator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido.infra.db import SessionFactory
from bushido.modules.domain import Ok
from bushido.modules.lifting.mapper import LiftingMapper
from bushido.modules.lifting.orm import LiftingSet, LiftingUnit
from bushido.modules.lifting.parser import LiftingParser
from bushido.modules.repo import UnitRepo
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
def service(session: Session) -> LogUnitService:
    parser = LiftingParser()
    mapper = LiftingMapper()
    repo = UnitRepo[LiftingUnit, LiftingSet](session, LiftingUnit, LiftingUnit.subunits)
    return LogUnitService(parser, mapper, repo)


def test_log_lifting_unit_success(service: LogUnitService, session: Session) -> None:
    line = "benchpress 100 5 180 100 5"
    res = service.log_unit(line)
    assert isinstance(res, Ok)
    assert res.value == "Unit confirmed"
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
