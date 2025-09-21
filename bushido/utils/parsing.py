import datetime
import re

# project imports
from bushido.core.conf import LOCAL_TIME_ZONE



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
