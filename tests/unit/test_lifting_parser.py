import datetime

import pytest
from freezegun import freeze_time

from bushido.core.result import Ok
from bushido.modules.dtypes import ParsedUnit
from bushido.modules.lifting.domain import LiftingSpec, SetSpec
from bushido.modules.lifting.parser import LiftingParser


@pytest.fixture
def parser():
    return LiftingParser(unit_name="squat")


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "100 5 180 100 5",
            ParsedUnit(
                name="squat",
                data=LiftingSpec(
                    sets=[
                        SetSpec(set_nr=0, weight=100.0, reps=5, rest=180.0),
                        SetSpec(set_nr=1, weight=100.0, reps=5, rest=0.0),
                    ]
                ),
                log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                comment=None,
            ),
        ),
        (
            "120 5",
            ParsedUnit(
                name="squat",
                data=LiftingSpec([SetSpec(set_nr=0, weight=120.0, reps=5, rest=0.0)]),
                log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                comment=None,
            ),
        ),
        (
            "150 3 300 160 2 90 100 20 # heavy day, 20reps at the end",
            ParsedUnit(
                name="squat",
                data=LiftingSpec(
                    sets=[
                        SetSpec(set_nr=0, weight=150.0, reps=3, rest=300.0),
                        SetSpec(set_nr=1, weight=160.0, reps=2.0, rest=90.0),
                        SetSpec(set_nr=2, weight=100.0, reps=20.0, rest=0.0),
                    ]
                ),
                log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                comment="heavy day, 20reps at the end",
            ),
        ),
        (
            "150 5 # just a single set",
            ParsedUnit(
                name="squat",
                data=LiftingSpec(
                    sets=[SetSpec(set_nr=0, weight=150.0, reps=5.0, rest=0.0)]
                ),
                log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                comment="just a single set",
            ),
        ),
    ],
)
@freeze_time("2020-01-01")
def test_correct_lifting_units(parser, line, expected):
    result = parser.parse(line)
    assert isinstance(result, Ok)
    parsed_unit = result.value
    assert parsed_unit == expected


# TODO move to clock injection
"""
class UnitParser(ABC, Generic[TUData]):
    def __init__(
        self,
        unit_name: str,
        clock: Callable[[], datetime] = datetime.datetime.now
    ) -> None:
        self.unit_name = unit_name
        self.clock = clock
"""
