import datetime

from bushido.units.parsing.dt_parse import (
    find_previous_sunday,
    parse_military_time_string,
    time_string_to_seconds,
)


def test_time_string_to_seconds_0() -> None:
    ts = "02:24:59"
    result = time_string_to_seconds(ts)
    assert 8699.0 == result


def test_time_string_to_seconds_1() -> None:
    ts = "1:02:03"
    result = time_string_to_seconds(ts)
    assert 3723.0 == result


def test_time_string_to_seconds_2() -> None:
    ts = "2:4:1"
    result = time_string_to_seconds(ts)
    assert 7441.0 == result


def test_time_string_to_seconds_3() -> None:
    ts = "32:29"
    result = time_string_to_seconds(ts)
    assert 1949.0 == result


def test_time_string_to_seconds_4() -> None:
    ts = "1:20"
    result = time_string_to_seconds(ts)
    assert 80.0 == result


def test_time_string_to_seconds_minutes() -> None:
    ts = "16"
    result = time_string_to_seconds(ts)
    assert 960.0 == result


def test_time_string_to_seconds_hours() -> None:
    ts = "2h"
    result = time_string_to_seconds(ts)
    assert 7200.0 == result


def test_time_string_to_seconds_seconds() -> None:
    ts = "32s"
    result = time_string_to_seconds(ts)
    assert 32.0 == result


def test_parse_military_time_string_0() -> None:
    ts = "1600"
    result = parse_military_time_string(ts)
    assert datetime.time(16, 0) == result


def test_find_previous_sunday() -> None:
    today = datetime.date(2025, 5, 1)
    prev_sunday = find_previous_sunday(today)
    assert prev_sunday == datetime.date(2025, 4, 27)
