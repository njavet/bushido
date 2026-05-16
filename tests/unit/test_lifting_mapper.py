import datetime

import pytest

from bushido.units.base import Unit
from bushido.units.lifting.db_model import LiftingUnitTable
from bushido.units.lifting.mapper import LiftingMapper
from bushido.units.lifting.unit import LiftingData


@pytest.fixture
def mapper() -> LiftingMapper:
    return LiftingMapper()


GYM_CASES = [
    (
        Unit(
            name="lifting",
            emoji="gorilla",
            data=LiftingData(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            comment=None,
        ),
        LiftingUnitTable(
            name="lifting",
            emoji="gorilla",
            log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            start_t=datetime.time(18, 0),
            end_t=datetime.time(19, 0),
            gym="nautilus",
        ),
    ),
]


@pytest.mark.parametrize("parsed_unit, unit", GYM_CASES)
def test_correct_to_orm_mapping(
    mapper: LiftingMapper, parsed_unit: Unit[LiftingData], unit: LiftingUnitTable
) -> None:
    u = mapper.to_orm(parsed_unit)
    assert isinstance(u, LiftingUnitTable)
    assert u.emoji == unit.emoji
    assert u.name == unit.name
    assert u.log_time == unit.log_time
    assert u.gym == unit.gym
    assert u.start_t == unit.start_t
    assert u.end_t == unit.end_t


@pytest.mark.parametrize("parsed_unit, unit", GYM_CASES)
def test_correct_from_orm_mapping(
    mapper: LiftingMapper, parsed_unit: Unit[LiftingData], unit: LiftingUnitTable
) -> None:
    pu = mapper.from_orm(unit)
    assert isinstance(pu, Unit)
    assert pu.emoji == unit.emoji
    assert pu.name == unit.name
    assert pu.comment == unit.comment
    assert pu.log_time == unit.log_time
    assert pu.data.start_t == unit.start_t
    assert pu.data.end_t == unit.end_t
    assert pu.data.gym == unit.gym
