import pytest

# project imports
from bushido.core.result import Ok, Err
from bushido.core.unit import UnitName
from bushido.domain.unit import UnitSpec, ParsedUnit
from bushido.service.parser.lifting import LiftingParser


@pytest.fixture
def parser():
    return LiftingParser()


@pytest.mark.parametrize('unit_spec, expected', [
    (UnitSpec(unit_name='squat',
              words=['100', '5', '180', '100', '5', '180', '100', '5']),
     ParsedUnit(unit_name=UnitName.squat,
                data={ 'weights': [100., 100., 100.],
                       'reps': [5., 5., 5.],
                       'rests': [180., 180.]},
                comment=None)),
    (UnitSpec(unit_name='squat',
              words=['120', '5', '300', '130', '2', '240', '110', '8']),
     ParsedUnit(unit_name=UnitName.squat,
                data={'weights': [120., 130., 110.],
                      'reps': [5., 2., 8.],
                      'rests': [300., 240.]},
                comment=None)),
    (UnitSpec(unit_name='squat',
              words=['150', '3', '300', '160', '2', '90', '100', '20'],
              comment="heavy day, 20reps at the end"),
     ParsedUnit(unit_name=UnitName.squat,
                data={'weights': [150., 160., 100.],
                      'reps': [3., 2., 20.],
                      'rests': [300., 90.]},
                comment='heavy day, 20reps at the end')),
    (UnitSpec(unit_name='deadlift',
              words=['150', '5'],
              comment='just a single set'),
     ParsedUnit(unit_name=UnitName.deadlift,
                data={'weights': [150.],
                      'reps': [5.],
                      'rests': []},
                comment='just a single set')),
    (UnitSpec(unit_name='benchpress',
              words=['90', '8', '240', '100', '5', '300', '110', '2']),
     ParsedUnit(unit_name=UnitName.benchpress,
                data={'weights': [90., 100., 110.],
                      'reps': [8., 5., 2.],
                      'rests': [240., 300.]},
                comment=None)),
])
def test_correct_lifting_units(parser, unit_spec, expected):
    result = parser.parse(unit_spec)
    assert isinstance(result, Ok)
    parsed_unit = result.value
    assert parsed_unit == expected
