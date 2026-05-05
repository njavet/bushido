import datetime

import pytest

from bushido.categories.dtypes import ParsedUnit
from bushido.categories.lifting import (
    LiftingMapper,
    LiftingSet,
    LiftingUnitTable,
)
from bushido.categories.lifting.parser import LiftingSpec, SetSpec


@pytest.fixture
def mapper() -> LiftingMapper:
    return LiftingMapper()


LIFTING_CASES = [
    (
        ParsedUnit(
            name="squat",
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
    parsed_unit: ParsedUnit[LiftingSpec],
    unit: LiftingUnitTable,
) -> None:
    u = mapper.to_orm(parsed_unit)
    assert isinstance(u, LiftingUnitTable)
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
    parsed_unit: ParsedUnit[LiftingSpec],
    unit: LiftingUnitTable,
) -> None:
    pu = mapper.from_orm(unit)
    assert isinstance(pu, ParsedUnit)
    assert pu.name == unit.name
    assert pu.comment == unit.comment
    assert pu.log_time == unit.log_time
    for i, ls in enumerate(pu.data.sets):
        assert isinstance(ls, SetSpec)
        assert ls.set_nr == unit.subunits[i].set_nr
        assert ls.weight == unit.subunits[i].weight
        assert ls.reps == unit.subunits[i].reps
        assert ls.rest == unit.subunits[i].rest
