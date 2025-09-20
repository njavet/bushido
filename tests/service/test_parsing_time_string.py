import datetime

import pytest

# project imports
from bushido.utils import parsing


def test_parse_time_string_HH_MM_SS_0():
    ts = '02:24:59'
    sec = parsing.parse_time_string(ts)
    assert 8699.0 == sec


def test_parse_time_string_HH_MM_SS_1():
    ts = '1:02:03'
    sec = parsing.parse_time_string(ts)
    assert 3723.0 == sec


def test_parse_time_string_HH_MM_SS_2():
    ts = '2:4:1'
    sec = parsing.parse_time_string(ts)
    assert 7441.0 == sec


def test_parse_time_string_MM_SS_0():
    ts = '32:29'
    sec = parsing.parse_time_string(ts)
    assert 1949.0 == sec


def test_parse_time_string_MM_SS_2():
    ts = '1:20'
    sec = parsing.parse_time_string(ts)
    assert 80.0 == sec


def test_parse_time_string_minutes():
    ts = '16'
    sec = parsing.parse_time_string(ts)
    assert 960.0 == sec


def test_parse_time_string_hours():
    ts = '2h'
    sec = parsing.parse_time_string(ts)
    assert 7200.0 == sec


def test_parse_time_string_seconds():
    ts = '32s'
    sec = parsing.parse_time_string(ts)
    assert 32.0 == sec


def test_parse_time_string_wrong_input_0():
    ts = 'not a valid time_string'
    with pytest.raises(ValueError):
        _ = parsing.parse_time_string(ts)


def test_parse_time_string_wrong_input_1():
    ts = '32five'
    with pytest.raises(ValueError):
        _ = parsing.parse_time_string(ts)


def test_parse_military_time_string_0():
    ts = '1600'
    mt = parsing.parse_military_time_string(ts)
    assert datetime.time(16, 0) == mt
