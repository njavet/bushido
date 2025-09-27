import pytest
from sqlalchemy.orm import Session
from sqlalchemy import select

from bushido.core.result import Err, Ok
from bushido.infra.db.conn import SessionFactory
from bushido.infra.db.model.lifting import LiftingUnit, LiftingSet
from bushido.infra.repo.base import UnitRepo
from bushido.service.log_unit import LogUnitService


@pytest.fixture
def session():
    sf = SessionFactory()
    yield sf.get_session_context()


@pytest.fixture
def service(session: Session):

def test_log_unit_happy_path_persists_unit_and_subunits(
    service: LogUnitService, session: Session
):
    line = 'bench_press 100 5 180 100 5'
    res = service.log_unit(line)
    assert isinstance(res, Ok)
    assert res.value == 'Unit confirmed'
    units = session.execute(select(LiftingUnit)).all()
    assert len(units) == 1
    assert units[0].name == 'bench_press'
    subs = session.execute(select(LiftingSet)).all()


def test_log_unit_without_subunits_still_persists(
    service: LogUnitService, session: Session
):
    res = service.log_unit('squat')
    assert isinstance(res, Ok)
    u = session.execute(select(LiftingSet)).one()
    assert u.name == 'squat'
    assert session.query(SubunitORM).count() == 0


def test_log_unit_rejects_empty_input(
    service: LogUnitService, session: Session
):
    res = service.log_unit('   ')
    assert isinstance(res, Err)


def test_log_unit_parse_error(
    service: LogUnitService, monkeypatch: pytest.MonkeyPatch
):
    class FailingParser(SimpleUnitParser):
        def parse(self, unit_spec: str) -> Result[ParsedUnit]:
            return Err('bad parse')

    monkeypatch.setattr(service, '_parser', FailingParser())
    res = service.log_unit('Deadlift:single')
    assert isinstance(res, Err)


def test_repo_failure_rolls_back(
    service: LogUnitService, session: Session, monkeypatch: pytest.MonkeyPatch
):
    # force a DB failure by violating NOT NULL on UnitORM.name after mapping
    class BadMapper(SimpleUnitMapper):
        def to_orm(self, parsed: ParsedUnit):
            u = UnitORM(name=None)  # type: ignore[arg-type]
            return u, []

    monkeypatch.setattr(service, '_mapper', BadMapper())
    res = service.log_unit('Anything')
    assert isinstance(res, Err)
    # ensure nothing committed
    assert session.query(UnitORM).count() == 0
