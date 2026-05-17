import datetime

import pytest

from bushido.domain.units import Data, Parser


@pytest.fixture
def parser() -> Parser:
    return Parser()


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (
            ("1800-1900", "nautilus"),
            Data(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs"),
            Data(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
        (
            ("1800-1900", "nautilus", "legs", "slow"),
            Data(
                start_t=datetime.time(18, 0),
                end_t=datetime.time(19, 0),
                gym="nautilus",
            ),
        ),
    ],
)
def test_correct_gym_units(
    parser: Parser, tokens: tuple[str, ...], expected: Data
) -> None:
    unit_data = parser.parse(tokens)
    assert unit_data == expected
