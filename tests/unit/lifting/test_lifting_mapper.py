import datetime

import pytest

from bushido.db.model.lifting import LiftingSet, LiftingUnitTable
from bushido.units.base import Unit
from bushido.units.lifting.mapper import LiftingMapper
from bushido.units.lifting.unit import LiftingData, SetData


@pytest.fixture
def mapper() -> LiftingMapper:
    return LiftingMapper()


LIFTING_CASES = [
    (
        Unit(
            name="squat",
            emoji="shinto",
            data=LiftingData(
                sets=[
                    SetData(set_nr=0, weight=100.0, reps=5, rest=180.0),
                    SetData(set_nr=1, weight=100.0, reps=5, rest=0.0),
                ],
                program=None,
                variant=None,
            ),
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            comment=None,
        ),
        LiftingUnitTable(
            name="squat",
            emoji="shinto",
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            sets=[
                LiftingSet(set_nr=0, weight=100.0, reps=5, rest=180.0),
                LiftingSet(set_nr=1, weight=100.0, reps=5, rest=0.0),
            ],
        ),
    ),
    (
        Unit(
            name="squat",
            emoji="shinto",
            data=LiftingData(
                sets=[
                    SetData(set_nr=0, weight=150.0, reps=3, rest=300.0),
                    SetData(set_nr=1, weight=100.0, reps=20.0, rest=0.0),
                ],
                program=None,
                variant=None,
            ),
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            comment="heavy day, 20reps at the end",
        ),
        LiftingUnitTable(
            name="squat",
            emoji="shinto",
            comment="heavy day, 20reps at the end",
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            sets=[
                LiftingSet(set_nr=0, weight=150.0, reps=3.0, rest=300.0),
                LiftingSet(set_nr=1, weight=100.0, reps=20.0, rest=0.0),
            ],
        ),
    ),
]


@pytest.mark.parametrize("parsed_unit, unit", LIFTING_CASES)
def test_correct_to_orm_mapping(
    mapper: LiftingMapper,
    parsed_unit: Unit[LiftingData],
    unit: LiftingUnitTable,
) -> None:
    u = mapper.to_orm(parsed_unit)
    assert isinstance(u, LiftingUnitTable)
    assert u.emoji == unit.emoji
    assert unit.name == u.name
    assert unit.comment == u.comment
    assert unit.log_time == u.log_time
    for i, ls in enumerate(u.sets):
        assert isinstance(ls, LiftingSet)
        assert ls.set_nr == unit.sets[i].set_nr
        assert ls.weight == unit.sets[i].weight
        assert ls.reps == unit.sets[i].reps
        assert ls.rest == unit.sets[i].rest


@pytest.mark.parametrize("parsed_unit, unit", LIFTING_CASES)
def test_correct_from_orm_mapping(
    mapper: LiftingMapper,
    parsed_unit: Unit[LiftingData],
    unit: LiftingUnitTable,
) -> None:
    pu = mapper.from_orm(unit)
    assert isinstance(pu, Unit)
    assert pu.emoji == unit.emoji
    assert pu.name == unit.name
    assert pu.comment == unit.comment
    assert pu.log_time == unit.log_time
    for i, ls in enumerate(pu.data.sets):
        assert isinstance(ls, SetData)
        assert ls.set_nr == unit.sets[i].set_nr
        assert ls.weight == unit.sets[i].weight
        assert ls.reps == unit.sets[i].reps
        assert ls.rest == unit.sets[i].rest
