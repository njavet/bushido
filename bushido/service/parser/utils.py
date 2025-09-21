import datetime
import re

from bushido.core.conf import DAY_START_HOUR

# project imports
from bushido.core.result import Err, Ok, Result


def time_string_to_seconds(time_string: str) -> Result[float]:
    """
    input string can be of the form:
    MM:SS, HH:MM:SS, <num>h, <num>s, <num> (-> default is minutes)
    :param time_string:
    :return seconds:

    """
    if time_string is None:
        return Err('time_string is None')

    values = time_string.split(':')
    if len(values) > 1:
        return colon_separated_time_string_to_seconds(values)

    try:
        m = float(values[0])
        return Ok(60 * m)
    except ValueError:
        if re.search(r'\d+h', values[0]):
            return Ok(60 * 60 * float(values[0][:-1]))
        elif re.search(r'\d+s', values[0]):
            return Ok(float(values[0][:-1]))
        else:
            return Err('colon time format error')


def colon_separated_time_string_to_seconds(values: list[str]) -> Result[float]:
    # format HH:MM:SS
    if len(values) == 3:
        try:
            h = float(values[0])
            m = float(values[1])
            s = float(values[2])
        except ValueError:
            return Err('colon time format error')
        else:
            return Ok(h * 60 * 60 + m * 60 + s)
    # format MM:SS
    elif len(values) == 2:
        try:
            m = float(values[0])
            s = float(values[1])
        except ValueError:
            return Err('colon time format error')
        else:
            return Ok(m * 60 + s)
    else:
        return Err('colon time format error')


def parse_military_time_string(time_string: str) -> Result[datetime.time]:
    # e.g. 1600 for 16:00
    if len(time_string) != 4:
        return Err('incorrect military time')
    try:
        hour = int(time_string[0:2])
        minutes = int(time_string[2:])
    except ValueError:
        return Err('incorrect military time')
    else:
        return Ok(datetime.time(hour, minutes))


def parse_start_end_time_string(
    time_string: str,
) -> Result[tuple[datetime.time, datetime.time]]:
    """
        the format is HHMM-HHMM as start time and end time
        "normal case": 0400 <= start < end <= 2359
        TODO start is before midnight, end is after midnight

    :param time_string:
    :return:
    """
    reg = re.search('[0-2][0-9][0-5][0-9]-[0-2][0-9][0-5][0-9]', time_string)
    if reg is None:
        return Err('wrong time format')
    s, e = reg.group().split('-')

    start_t_res = parse_military_time_string(s)
    end_t_res = parse_military_time_string(e)
    if isinstance(start_t_res, Ok):
        start_t = start_t_res.value
    else:
        return start_t_res
    if isinstance(end_t_res, Ok):
        end_t = end_t_res.value
    else:
        return end_t_res
    return Ok(value=(start_t, end_t))


def get_bushido_date_from_datetime(dt: datetime.datetime) -> datetime.date:
    if 0 <= dt.hour < DAY_START_HOUR:
        return dt.date() - datetime.timedelta(days=1)
    else:
        return dt.date()


def find_previous_sunday(dt: datetime.date) -> datetime.date:
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


def find_next_saturday(dt: datetime.date) -> datetime.date:
    if dt.weekday() != 6:
        days = 5 - dt.weekday()
        return dt + datetime.timedelta(days=days)
    else:
        return dt + datetime.timedelta(days=6)
