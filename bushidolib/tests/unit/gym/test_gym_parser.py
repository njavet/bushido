import datetime

import pytest

from bushidolib.category.gym import GymUnit, build_gym_unit
from bushidolib.schema.unit import RawUnit


@pytest.mark.parametrize(
    ("raw_unit", "lt", "expected"),
    [
        (
            RawUnit(name="lifting", tokens=("1800-1900", "nautilus")),
            datetime.datetime(2026, 1, 1, 1, 0, 1, tzinfo=datetime.UTC),
            GymUnit(
                name="lifting",
                log_time=datetime.datetime(2026, 1, 1, 1, 0, 1, tzinfo=datetime.UTC),
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
        (
            RawUnit(name="yoga", tokens=("2300-0030", "nautilus")),
            datetime.datetime(2026, 1, 1, 1, 0, 1, tzinfo=datetime.UTC),
            GymUnit(
                name="yoga",
                log_time=datetime.datetime(2026, 1, 1, 1, 0, 1, tzinfo=datetime.UTC),
                start_t=datetime.time(23, 0),
                end_t=datetime.time(0, 30),
                gym="nautilus",
            ),
        ),
    ],
)
def test_correct_gym_units(
    raw_unit: RawUnit, lt: datetime.datetime, expected: GymUnit
) -> None:
    unit = build_gym_unit(raw_unit, log_time=lt)
    assert unit == expected
