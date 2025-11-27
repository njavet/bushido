import datetime

import pytest
from freezegun import freeze_time

from bushido.modules.dtypes import Ok, ParsedUnit
from bushido.modules.wimhof import RoundSpec, WimhofParser, WimhofSpec


@pytest.fixture
def parser():
    return WimhofParser(unit_name="wimhof")


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "30 90 30 120 30 150",
            ParsedUnit(
                name="wimhof",
                data=WimhofSpec(
                    rounds=[
                        RoundSpec(round_nr=0, breaths=30, retention=90),
                        RoundSpec(round_nr=1, breaths=30, retention=120),
                        RoundSpec(round_nr=2, breaths=30, retention=150),
                    ]
                ),
                log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                comment=None,
            ),
        ),
    ],
)
@freeze_time("2020-01-01")
def test_correct_wimhof_unit(parser, line, expected):
    result = parser.parse(line)
    assert isinstance(result, Ok)
    parsed_unit = result.value
    assert parsed_unit == expected
