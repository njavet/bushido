import pytest

from bushido.category.lifting.domain import LiftingSpec, SetSpec
from bushido.category.lifting.parser import LiftingParser
from bushido.core.exceptions import ParsingError


@pytest.fixture
def parser() -> LiftingParser:
    return LiftingParser()


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (
            ("100", "5", "180", "100", "5"),
            LiftingSpec(
                sets=[
                    SetSpec(set_nr=0, weight=100.0, reps=5, rest=180.0),
                    SetSpec(set_nr=1, weight=100.0, reps=5, rest=0.0),
                ]
            ),
        ),
        (
            ("120", "5"),
            LiftingSpec([SetSpec(set_nr=0, weight=120.0, reps=5, rest=0.0)]),
        ),
        (
            ("150", "3", "300", "160", "2", "90", "100", "20"),
            LiftingSpec(
                sets=[
                    SetSpec(set_nr=0, weight=150.0, reps=3, rest=300.0),
                    SetSpec(set_nr=1, weight=160.0, reps=2.0, rest=90.0),
                    SetSpec(set_nr=2, weight=100.0, reps=20.0, rest=0.0),
                ]
            ),
        ),
    ],
)
def test_correct_lifting_units(
    parser: LiftingParser, tokens: tuple[str, ...], expected: LiftingSpec
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
