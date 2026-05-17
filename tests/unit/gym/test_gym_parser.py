import datetime

import pytest

from bushido.domain.units.gym import GymData, GymParser


@pytest.fixture
def parser() -> GymParser:
    return GymParser()


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (
            ("1800-1900", "nautilus"),
            GymData(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs"),
            GymData(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs", "slow"),
            GymData(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
    ],
)
def test_correct_gym_units(
    parser: GymParser, tokens: tuple[str, ...], expected: GymData
) -> None:
    unit_data = parser.parse(tokens)
    assert unit_data == expected
