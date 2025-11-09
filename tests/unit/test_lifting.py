import pytest

from bushido.modules.domain import Ok, ParsedUnit
from bushido.modules.lifting.domain import ExerciseSpec, SetSpec
from bushido.modules.lifting.parser import LiftingParser


@pytest.fixture
def parser():
    return LiftingParser()


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "squat 100 5 180 100 5",
            ParsedUnit(
                name="squat",
                data=ExerciseSpec(
                    sets=[
                        SetSpec(set_nr=0, weight=100.0, reps=5, rest=180.0),
                        SetSpec(set_nr=1, weight=100.0, reps=5, rest=0.0),
                    ]
                ),
                comment=None,
            ),
        ),
        (
            "squat 120 5",
            ParsedUnit(
                name="squat",
                data=ExerciseSpec(
                    sets=[SetSpec(set_nr=0, weight=120.0, reps=5, rest=0.0)]
                ),
                comment=None,
            ),
        ),
        (
            "squat 150 3 300 160 2 90 100 20 # heavy day, 20reps at the end",
            ParsedUnit(
                name="squat",
                data=ExerciseSpec(
                    sets=[
                        SetSpec(set_nr=0, weight=150.0, reps=3, rest=300.0),
                        SetSpec(set_nr=1, weight=160.0, reps=2.0, rest=90.0),
                        SetSpec(set_nr=2, weight=100.0, reps=20.0, rest=0.0),
                    ]
                ),
                comment="heavy day, 20reps at the end",
            ),
        ),
        (
            "deadlift 150 5 # just a single set",
            ParsedUnit(
                name="deadlift",
                data=ExerciseSpec(
                    sets=[SetSpec(set_nr=0, weight=150.0, reps=5.0, rest=0.0)]
                ),
                comment="just a single set",
            ),
        ),
    ],
)
def test_correct_lifting_units(parser, line, expected):
    result = parser.parse(line)
    assert isinstance(result, Ok)
    parsed_unit = result.value
    assert parsed_unit == expected
