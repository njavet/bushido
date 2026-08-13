import datetime
from collections.abc import Iterator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido_server.main import init_db
from bushido_server.persistence import SessionFactory
from bushido_server.persistence.models import LiftingSet, LiftingUnitTable
from bushido_server.schema.log_req import LiftingLogUnitRequest
from bushido_server.service import log_unit


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


def test_log_lifting_unit_success(session: Session) -> None:
    lr = LiftingLogUnitRequest(
        user_name="test",
        log_time=datetime.datetime.now(),
        unit_name="benchpress",
        tokens=("100", "5", "180", "100", "5"),
    )
    log_unit(lr, session)
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
