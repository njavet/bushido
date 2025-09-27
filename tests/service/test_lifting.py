import pytest

# project imports
from bushido.core.result import Ok
from bushido.domain.lifting import ExerciseSpec, SetSpec
from bushido.domain.unit import ParsedUnit, UnitSpec
from bushido.service.parser.lifting import LiftingParser


@pytest.fixture
def parser():
    return LiftingParser()


@pytest.mark.parametrize(
    'unit_spec, expected',
    [
        (
            UnitSpec(name='squat', words=['100', '5', '180', '100', '5']),
            ParsedUnit(
                name='squat',
                data=ExerciseSpec(
                    sets=[
                        SetSpec(weight=100.0, reps=5, rest=180.0),
                        SetSpec(weight=100.0, reps=5, rest=0.0),
                    ]
                ),
                comment=None,
            ),
        ),
        (
            UnitSpec(name='squat', words=['120', '5']),
            ParsedUnit(
                name='squat',
                data=ExerciseSpec(
                    sets=[SetSpec(weight=120.0, reps=5, rest=0.0)]
                ),
                comment=None,
            ),
        ),
        (
            UnitSpec(
                name='squat',
                words=['150', '3', '300', '160', '2', '90', '100', '20'],
                comment='heavy day, 20reps at the end',
            ),
            ParsedUnit(
                name='squat',
                data=ExerciseSpec(
                    sets=[
                        SetSpec(weight=150.0, reps=3, rest=300.0),
                        SetSpec(weight=160.0, reps=2.0, rest=90.0),
                        SetSpec(weight=100.0, reps=20.0, rest=0.0),
                    ]
                ),
                comment='heavy day, 20reps at the end',
            ),
        ),
        (
            UnitSpec(
                name='deadlift',
                words=['150', '5'],
                comment='just a single set',
            ),
            ParsedUnit(
                name='deadlift',
                data=ExerciseSpec(
                    sets=[SetSpec(weight=150.0, reps=5.0, rest=0.0)]
                ),
                comment='just a single set',
            ),
        ),
    ],
)
def test_correct_lifting_units(parser, unit_spec, expected):
    result = parser.parse(unit_spec)
    assert isinstance(result, Ok)
    parsed_unit = result.value
    assert parsed_unit == expected
