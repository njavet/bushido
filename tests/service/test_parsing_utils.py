import datetime

# project imports
from bushido.service.parser.utils import (
    find_previous_sunday,
    parse_military_time_string,
    parse_time_string,
)


def test_parse_time_string_HH_MM_SS_0():
    ts = '02:24:59'
    sec = parse_time_string(ts)
    assert 8699.0 == sec


def test_parse_time_string_HH_MM_SS_1():
    ts = '1:02:03'
    sec = parse_time_string(ts)
    assert 3723.0 == sec


def test_parse_time_string_HH_MM_SS_2():
    ts = '2:4:1'
    sec = parse_time_string(ts)
    assert 7441.0 == sec


def test_parse_time_string_MM_SS_0():
    ts = '32:29'
    sec = parse_time_string(ts)
    assert 1949.0 == sec


def test_parse_time_string_MM_SS_2():
    ts = '1:20'
    sec = parse_time_string(ts)
    assert 80.0 == sec


def test_parse_time_string_minutes():
    ts = '16'
    sec = parse_time_string(ts)
    assert 960.0 == sec


def test_parse_time_string_hours():
    ts = '2h'
    sec = parse_time_string(ts)
    assert 7200.0 == sec


def test_parse_time_string_seconds():
    ts = '32s'
    sec = parse_time_string(ts)
    assert 32.0 == sec


def test_parse_military_time_string_0():
    ts = '1600'
    mt = parse_military_time_string(ts)
    assert datetime.time(16, 0) == mt


def test_find_previous_sunday():
    today = datetime.date(2025, 5, 1)
    prev_sunday = find_previous_sunday(today)
    assert prev_sunday == datetime.date(2025, 4, 27)
