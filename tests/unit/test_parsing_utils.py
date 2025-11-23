import datetime

from bushido.modules.base import Ok
from bushido.modules.parsing_utils import (
    find_previous_sunday,
    parse_military_time_string,
    time_string_to_seconds,
)


def test_time_string_to_seconds_HH_MM_SS_0():
    ts = "02:24:59"
    result = time_string_to_seconds(ts)
    assert isinstance(result, Ok)
    assert 8699.0 == result.value


def test_time_string_to_seconds_HH_MM_SS_1():
    ts = "1:02:03"
    result = time_string_to_seconds(ts)
    assert isinstance(result, Ok)
    assert 3723.0 == result.value


def test_time_string_to_seconds_HH_MM_SS_2():
    ts = "2:4:1"
    result = time_string_to_seconds(ts)
    assert isinstance(result, Ok)
    assert 7441.0 == result.value


def test_time_string_to_seconds_MM_SS_0():
    ts = "32:29"
    result = time_string_to_seconds(ts)
    assert isinstance(result, Ok)
    assert 1949.0 == result.value


def test_time_string_to_seconds_MM_SS_2():
    ts = "1:20"
    result = time_string_to_seconds(ts)
    assert isinstance(result, Ok)
    assert 80.0 == result.value


def test_time_string_to_seconds_minutes():
    ts = "16"
    result = time_string_to_seconds(ts)
    assert isinstance(result, Ok)
    assert 960.0 == result.value


def test_time_string_to_seconds_hours():
    ts = "2h"
    result = time_string_to_seconds(ts)
    assert isinstance(result, Ok)
    assert 7200.0 == result.value


def test_time_string_to_seconds_seconds():
    ts = "32s"
    result = time_string_to_seconds(ts)
    assert isinstance(result, Ok)
    assert 32.0 == result.value


def test_parse_military_time_string_0():
    ts = "1600"
    result = parse_military_time_string(ts)
    assert isinstance(result, Ok)
    assert datetime.time(16, 0) == result.value


def test_find_previous_sunday():
    today = datetime.date(2025, 5, 1)
    prev_sunday = find_previous_sunday(today)
    assert prev_sunday == datetime.date(2025, 4, 27)
