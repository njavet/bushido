import datetime

import pytest

from bushido.units.lifting.parser import LiftingParser
from bushido.units.lifting.unit import LiftingData


@pytest.fixture
def parser() -> LiftingParser:
    return LiftingParser()


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (
            ("1800-1900", "nautilus"),
            LiftingData(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs"),
            LiftingData(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs", "slow"),
            LiftingData(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
    ],
)
def test_correct_gym_units(
    parser: LiftingParser, tokens: tuple[str, ...], expected: LiftingData
) -> None:
    unit_data = parser.parse(tokens)
    assert unit_data == expected
