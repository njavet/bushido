from collections.abc import Iterator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido.application.registry import build_registry
from bushido.application.service import LogUnitService
from bushido.main import init_db
from bushido.persistence.models.lifting import LiftingSet, LiftingUnitTable
from bushido.persistence.sf import SessionFactory


@pytest.fixture(scope="session")
def session_factory() -> SessionFactory:
    sf = SessionFactory("sqlite+pysqlite:///:memory:")
    init_db(engine=sf.engine)
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
    return LogUnitService(registry=build_registry())


def test_log_lifting_unit_success(service: LogUnitService, session: Session) -> None:
    line = "benchpress 100 5 180 100 5"
    service.log_unit(line, session)
    units = session.scalars(select(LiftingUnitTable)).all()
    assert len(units) == 1
    assert units[0].name == "benchpress"
    subs = session.scalars(select(LiftingSet)).all()
    assert len(subs) == 2
    assert subs[0].weight == 100
    assert subs[0].reps == 5
    assert subs[0].rest == 180
    assert subs[1].weight == 100
    assert subs[1].reps == 5
