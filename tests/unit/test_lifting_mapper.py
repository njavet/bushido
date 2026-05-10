import datetime

import pytest

from bushido.categories.lifting.domain import LiftingSpec, LiftingUnit, SetSpec
from bushido.categories.lifting.mapper import LiftingMapper
from bushido.categories.lifting.orm import LiftingSet, LiftingUnitTable
from bushido.core.dtypes import ParsedUnit


@pytest.fixture
def mapper() -> LiftingMapper:
    return LiftingMapper()


LIFTING_CASES = [
    (
        ParsedUnit(
            name="squat",
            emoji="shinto",
            data=LiftingSpec(
                sets=[
                    SetSpec(set_nr=0, weight=100.0, reps=5, rest=180.0),
                    SetSpec(set_nr=1, weight=100.0, reps=5, rest=0.0),
                ]
            ),
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            comment=None,
        ),
        LiftingUnitTable(
            name="squat",
            emoji="shinto",
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            subunits=[
                LiftingSet(set_nr=0, weight=100.0, reps=5, rest=180.0),
                LiftingSet(set_nr=1, weight=100.0, reps=5, rest=0.0),
            ],
        ),
    ),
    (
        ParsedUnit(
            name="squat",
            emoji="shinto",
            data=LiftingSpec(
                sets=[
                    SetSpec(set_nr=0, weight=150.0, reps=3, rest=300.0),
                    SetSpec(set_nr=1, weight=100.0, reps=20.0, rest=0.0),
                ]
            ),
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            comment="heavy day, 20reps at the end",
        ),
        LiftingUnitTable(
            name="squat",
            emoji="shinto",
            comment="heavy day, 20reps at the end",
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            subunits=[
                LiftingSet(set_nr=0, weight=150.0, reps=3.0, rest=300.0),
                LiftingSet(set_nr=1, weight=100.0, reps=20.0, rest=0.0),
            ],
        ),
    ),
]


@pytest.mark.parametrize("parsed_unit, unit", LIFTING_CASES)
def test_correct_to_orm_mapping(
    mapper: LiftingMapper,
    parsed_unit: LiftingUnit,
    unit: LiftingUnitTable,
) -> None:
    u = mapper.to_orm(parsed_unit)
    assert isinstance(u, LiftingUnitTable)
    assert u.emoji == unit.emoji
    assert unit.name == u.name
    assert unit.comment == u.comment
    assert unit.log_time == u.log_time
    for i, ls in enumerate(u.subunits):
        assert isinstance(ls, LiftingSet)
        assert ls.set_nr == unit.subunits[i].set_nr
        assert ls.weight == unit.subunits[i].weight
        assert ls.reps == unit.subunits[i].reps
        assert ls.rest == unit.subunits[i].rest


@pytest.mark.parametrize("parsed_unit, unit", LIFTING_CASES)
def test_correct_from_orm_mapping(
    mapper: LiftingMapper,
    parsed_unit: LiftingUnit,
    unit: LiftingUnitTable,
) -> None:
    pu = mapper.from_orm(unit)
    assert isinstance(pu, ParsedUnit)
    assert pu.emoji == unit.emoji
    assert pu.name == unit.name
    assert pu.comment == unit.comment
    assert pu.log_time == unit.log_time
    for i, ls in enumerate(pu.data.sets):
        assert isinstance(ls, SetSpec)
        assert ls.set_nr == unit.subunits[i].set_nr
        assert ls.weight == unit.subunits[i].weight
        assert ls.reps == unit.subunits[i].reps
        assert ls.rest == unit.subunits[i].rest
