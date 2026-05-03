import datetime

import pytest

from bushido.core.result import Ok
from bushido.units.gym import GymParser, GymSpec


@pytest.fixture
def parser() -> GymParser:
    return GymParser()


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (
            ("1800-1900", "nautilus"),
            GymSpec(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                location="nautilus",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs"),
            GymSpec(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                location="nautilus",
                training="legs",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs", "slow"),
            GymSpec(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                location="nautilus",
                training="legs",
                focus="slow",
            ),
        ),
    ],
)
def test_correct_gym_units(
    parser: GymParser, tokens: tuple[str, ...], expected: GymSpec
) -> None:
    result = parser.parse(tokens)
    assert isinstance(result, Ok)
    unit_data = result.value
    assert unit_data == expected
