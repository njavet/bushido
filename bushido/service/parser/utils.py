import datetime
import re

import pytz

# project imports
from bushido.core.conf import DAY_START_HOUR, LOCAL_TIME_ZONE


def parse_time_string(time_string: str) -> float | None:
    """
    input string can be of the form:
    MM:SS, HH:MM:SS, <num>h, <num>s, <num> (-> default is minutes)
    :param time_string:
    :return seconds:

    """
    assert time_string is not None

    values = time_string.split(':')
    if len(values) > 1:
        return parse_colon_separated_time_string(values)

    try:
        m = float(values[0])
        return 60 * m
    except ValueError:
        if re.search(r'\d+h', values[0]):
            return 60 * 60 * float(values[0][:-1])
        if re.search(r'\d+s', values[0]):
            return float(values[0][:-1])


def parse_colon_separated_time_string(values: list[str]) -> float:
    # format HH:MM:SS
    if len(values) == 3:
        try:
            h = float(values[0])
            m = float(values[1])
            s = float(values[2])
        except ValueError:
            raise ValueError('colon time format error')
        else:
            return h * 60 * 60 + m * 60 + s
    # format MM:SS
    elif len(values) == 2:
        try:
            m = float(values[0])
            s = float(values[1])
        except ValueError:
            raise ValueError('colon time format error')
        else:
            return m * 60 + s
    else:
        raise ValueError('colon time format error')


def parse_military_time_string(time_string: str) -> datetime.time:
    # e.g. 1600 for 16:00
    if len(time_string) != 4:
        raise ValueError('incorrect military time')
    try:
        hour = int(time_string[0:2])
        minutes = int(time_string[2:])
    except ValueError:
        raise ValueError('incorrect military time')
    else:
        return datetime.time(hour, minutes)


def parse_start_end_time_string(
    time_string: str,
) -> tuple[datetime.time, datetime.time]:
    """
        the format is HHMM-HHMM as start time and end time
        "normal case": 0400 <= start < end <= 2359
        TODO start is before midnight, end is after midnight

    :param time_string:
    :return:
    """
    reg = re.search('[0-2][0-9][0-5][0-9]-[0-2][0-9][0-5][0-9]', time_string)
    try:
        s, e = reg.group().split('-')
    except AttributeError:
        raise ValueError('wrong time format')

    start_t = parse_military_time_string(s)
    end_t = parse_military_time_string(e)

    return start_t, end_t


def parse_datetime_to_timestamp(words, option='--dt') -> tuple[int, list[str]]:
    """
    dt format: %Y.%m.%d-%H:%M
    """
    try:
        ind = words.index(option)
    except ValueError:
        now = datetime.datetime.now().replace(tzinfo=LOCAL_TIME_ZONE)
        timestamp = int(now.timestamp())
        return timestamp, words
    try:
        dt_str = words[ind + 1]
    except IndexError:
        raise ValueError('no datetime')

    try:
        dt = datetime.datetime.strptime(dt_str, '%Y.%m.%d-%H%M')
    except ValueError:
        raise ValueError('wrong time format')

    dt = dt.replace(tzinfo=LOCAL_TIME_ZONE)
    words = words[:ind] + words[ind + 2 :]
    return int(dt.timestamp()), words


def get_datetime_from_timestamp(
    timestamp: int, timezone='Europe/Zurich'
) -> datetime.datetime:
    cet_timezone = pytz.timezone(timezone)
    cet_dt = datetime.datetime.fromtimestamp(timestamp, cet_timezone)
    return cet_dt


def get_bushido_date_from_timestamp(timestamp: int):
    local_dt = datetime.datetime.fromtimestamp(timestamp, tz=LOCAL_TIME_ZONE)
    return get_bushido_date_from_datetime(local_dt)


def get_bushido_date_from_datetime(dt: datetime.datetime) -> datetime.date:
    if 0 <= dt.hour < DAY_START_HOUR:
        return dt.date() - datetime.timedelta(days=1)
    else:
        return dt.date()


def create_unit_response_dt(timestamp):
    dt = get_datetime_from_timestamp(timestamp)
    bushido_date = get_bushido_date_from_datetime(dt)
    hms = dt.strftime('%H%M')
    return bushido_date, hms


def find_previous_sunday(dt):
    """
    Finds the previous sunday of the given date
    e.g. input: 01.01.2020
    returns: 29.12.2019

    """
    if dt.weekday() != 6:
        days = dt.weekday() + 1
        return dt - datetime.timedelta(days=days)
    else:
        return dt


def find_next_saturday(dt):
    if dt.weekday() != 6:
        days = 5 - dt.weekday()
        return dt + datetime.timedelta(days=days)
    else:
        return dt + datetime.timedelta(days=6)
