import datetime

import pytest
from freezegun import freeze_time

from bushido.core.dtypes import ParsedUnit
from bushido.core.result import Err, Ok
from bushido.modules.gym import GymParser, GymSpec


@pytest.fixture
def parser():
    return GymParser(unit_name="weights")


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "1800-1900 nautilus",
            ParsedUnit(
                name="weights",
                data=GymSpec(
                    start_t=datetime.time(18, 0),
                    end_t=datetime.time(19, 0),
                    location="nautilus",
                ),
                log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                comment=None,
            ),
        ),
        (
            "1800-1900 nautilus # test training",
            ParsedUnit(
                name="weights",
                data=GymSpec(
                    start_t=datetime.time(18, 0),
                    end_t=datetime.time(19, 0),
                    location="nautilus",
                ),
                log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                comment="test training",
            ),
        ),
        (
            "1800-1900 nautilus legs # test training",
            ParsedUnit(
                name="weights",
                data=GymSpec(
                    start_t=datetime.time(18, 0),
                    end_t=datetime.time(19, 0),
                    location="nautilus",
                    training="legs",
                ),
                log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                comment="test training",
            ),
        ),
        (
            "1800-1900 nautilus legs slow # test training",
            ParsedUnit(
                name="weights",
                data=GymSpec(
                    start_t=datetime.time(18, 0),
                    end_t=datetime.time(19, 0),
                    location="nautilus",
                    training="legs",
                    focus="slow",
                ),
                log_time=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                comment="test training",
            ),
        ),
    ],
)
@freeze_time("2020-01-01")
def test_correct_gym_units(parser, line, expected):
    result = parser.parse(line)
    assert isinstance(result, Ok)
    parsed_unit = result.value
    assert parsed_unit == expected


@pytest.mark.parametrize(
    "line",
    [
        "",
    ],
)
def test_invalid_gym_units(parser, line):
    result = parser.parse(line)
    assert isinstance(result, Err)
