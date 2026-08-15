from collections.abc import Iterator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido_server.persistence import SessionFactory
from bushido_server.persistence.models import (
    Base,
    LiftingSet,
    LiftingUnitTable,
    UnitCategoryTable,
    UnitSettingTable,
)
from bushido_server.service import log_unit
from bushidolib.constants import UnitCategory


@pytest.fixture(scope="session")
def session_factory() -> SessionFactory:
    sf = SessionFactory("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(sf.engine)
    with sf.session() as session:
        session.add(UnitCategoryTable(name=UnitCategory.LIFTING))
        session.commit()
        session.add(UnitSettingTable(name="benchpress", category_id=1))
        session.commit()
    return sf


@pytest.fixture
def session(session_factory: SessionFactory) -> Iterator[Session]:
    with session_factory.session() as s:
        try:
            yield s
        finally:
            s.close()


def test_log_lifting_unit_success(session: Session) -> None:
    line = "benchpress 100 5 180 100 5"
    _ = log_unit(line, session)
    units = session.scalars(select(LiftingUnitTable)).all()
    assert len(units) == 1
    subs = session.scalars(select(LiftingSet)).all()
    assert len(subs) == 2
    assert subs[0].weight == 100
    assert subs[0].reps == 5
    assert subs[0].rest == 180
    assert subs[1].weight == 100
    assert subs[1].reps == 5
