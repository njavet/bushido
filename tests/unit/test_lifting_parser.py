import datetime

import pytest
from bushido.category.gym.domain import GymSpec
from bushido.category.gym.parser import GymParser


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
                gym="nautilus",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs"),
            GymSpec(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs", "slow"),
            GymSpec(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
    ],
)
def test_correct_gym_units(
    parser: GymParser, tokens: tuple[str, ...], expected: GymSpec
) -> None:
    unit_data = parser.parse(tokens)
    assert unit_data == expected
