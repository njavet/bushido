import datetime

import pytest

from bushido.core.dtypes import ParsedUnit
from bushido.modules.gym import GymMapper, GymSpec, GymUnit


@pytest.fixture
def mapper():
    return GymMapper()


GYM_CASES = [
    (
        ParsedUnit(
            name="weights",
            data=GymSpec(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                location="nautilus",
            ),
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            comment=None,
        ),
        GymUnit(
            name="weights",
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            start_t=datetime.time(18, 0),
            end_t=datetime.time(19, 0),
            location="nautilus",
        ),
    ),
]


@pytest.mark.parametrize("parsed_unit, unit", GYM_CASES)
def test_correct_to_orm_mapping(mapper, parsed_unit, unit):
    u, _ = mapper.to_orm(parsed_unit)
    assert isinstance(u, GymUnit)
    assert u.name == unit.name
    assert u.log_time == unit.log_time
    assert u.location == unit.location
    assert u.start_t == unit.start_t
    assert u.end_t == unit.end_t


@pytest.mark.parametrize("parsed_unit, unit", GYM_CASES)
def test_correct_from_orm_mapping(mapper, parsed_unit, unit):
    pu = mapper.from_orm((unit, []))
    assert isinstance(pu, ParsedUnit)
    assert pu.name == unit.name
    assert pu.comment == unit.comment
    assert pu.log_time == unit.log_time
    assert pu.data.start_t == unit.start_t
    assert pu.data.end_t == unit.end_t
    assert pu.data.location == unit.location
