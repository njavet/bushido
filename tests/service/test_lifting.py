import pytest

# project imports
from bushido.core.result import Ok, Err
from bushido.core.unit import UnitName
from bushido.domain.base import UnitSpec, ParsedUnit
from bushido.domain.lifting import SetSpec, Exercise
from bushido.service.parser.lifting import LiftingParser


@pytest.fixture
def parser():
    return LiftingParser()


@pytest.mark.parametrize('unit_spec, expected', [
    (UnitSpec(unit_name='squat',
              words=['100', '5', '180', '100', '5']),
    ParsedUnit(unit_name=UnitName.squat,
               data=Exercise(sets=[
                   SetSpec(weight=100.,
                           reps=5,
                           rest=180.),
                   SetSpec(weight=100.,
                           reps=5,
                           rest=0.)]),
               comment=None),
    ),
    (UnitSpec(unit_name='squat',
              words=['120', '5']),
    ParsedUnit(unit_name=UnitName.squat,
               data=Exercise(sets=[
                   SetSpec(weight=120.,
                           reps=5,
                           rest=0.)]),
                   comment=None)
    ),
    (UnitSpec(unit_name='squat',
              words=['150', '3', '300', '160', '2', '90', '100', '20'],
              comment="heavy day, 20reps at the end"),
    ParsedUnit(unit_name=UnitName.squat,
               data=Exercise(sets=[
                   SetSpec(weight=150.,
                           reps=3,
                           rest=300.),
                   SetSpec(weight=160.,
                           reps=2.,
                           rest=90.),
                   SetSpec(weight=100.,
                           reps=20.,
                           rest=0.),
               ]),
               comment='heavy day, 20reps at the end')
    ),
    (UnitSpec(unit_name='deadlift',
              words=['150', '5'],
              comment='just a single set'),
    ParsedUnit(unit_name=UnitName.deadlift,
               data=Exercise(sets=[
                   SetSpec(weight=150.,
                           reps=5.,
                           rest=0.)
               ]),
               comment='just a single set')
    ),
])
def test_correct_lifting_units(parser, unit_spec, expected):
    result = parser.parse(unit_spec)
    assert isinstance(result, Ok)
    parsed_unit = result.value
    print('parsed_unit', parsed_unit)
    assert parsed_unit == expected
