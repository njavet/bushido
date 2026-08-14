import datetime
import zoneinfo
from collections.abc import Iterator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido_server.persistence import SessionFactory
from bushido_server.persistence.models import LiftingSet, LiftingUnitTable
from bushido_server.service import log_unit
from bushidolib.contracts.log_req import LiftingLogUnitRequest


@pytest.fixture(scope="session")
def session_factory() -> SessionFactory:
    return SessionFactory("sqlite+pysqlite:///:memory:")


@pytest.fixture
def session(session_factory: SessionFactory) -> Iterator[Session]:
    with session_factory.session() as s:
        try:
            yield s
        finally:
            s.close()


@pytest.mark.skip("empty db")
def test_log_lifting_unit_success(session: Session) -> None:
    lr = LiftingLogUnitRequest(
        log_time=datetime.datetime.now(zoneinfo.ZoneInfo("UTC")),
        unit_name="benchpress",
        tokens=("100", "5", "180", "100", "5"),
    )
    log_unit(lr, session)
    units = session.scalars(select(LiftingUnitTable)).all()
    assert len(units) == 1
    subs = session.scalars(select(LiftingSet)).all()
    assert len(subs) == 2
    assert subs[0].weight == 100
    assert subs[0].reps == 5
    assert subs[0].rest == 180
    assert subs[1].weight == 100
    assert subs[1].reps == 5
