import pytest

from bushido.units.exceptions import ParsingError
from bushido.units.lifting.parser import LiftingParser
from bushido.units.lifting.unit import LiftingData, SetData


@pytest.fixture
def parser() -> LiftingParser:
    return LiftingParser()


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (
            ("100", "5", "180", "100", "5"),
            LiftingData(
                sets=[
                    SetData(set_nr=0, weight=100.0, reps=5, rest=180.0),
                    SetData(set_nr=1, weight=100.0, reps=5, rest=0.0),
                ],
                program=None,
                variant=None,
            ),
        ),
        (
            ("120", "5"),
            LiftingData(
                sets=[SetData(set_nr=0, weight=120.0, reps=5, rest=0.0)],
                program=None,
                variant=None,
            ),
        ),
        (
            ("150", "3", "300", "160", "2", "90", "100", "20"),
            LiftingData(
                sets=[
                    SetData(set_nr=0, weight=150.0, reps=3, rest=300.0),
                    SetData(set_nr=1, weight=160.0, reps=2.0, rest=90.0),
                    SetData(set_nr=2, weight=100.0, reps=20.0, rest=0.0),
                ],
                program=None,
                variant=None,
            ),
        ),
    ],
)
def test_correct_lifting_units(
    parser: LiftingParser, tokens: tuple[str, ...], expected: LiftingData
) -> None:
    unit_data = parser.parse(tokens)
    assert unit_data == expected


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (("asdf", "5", "180"), "invalid weight"),
        (("120", "f9"), "invalid reps"),
        (("150", "3", "f22"), "invalid rest"),
    ],
)
def test_correct_error_message(
    parser: LiftingParser, tokens: tuple[str, ...], expected: str
) -> None:
    with pytest.raises(ParsingError, match=expected):
        _ = parser.parse(tokens)
