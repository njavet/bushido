import datetime
import re

from bushido.core.exceptions import ParsingError


def time_string_to_seconds(time_string: str) -> float:
    """
    the input string can be of the form:
    MM:SS, HH:MM:SS, <num>h, <num>s, <num> (-> default is minutes)
    :param time_string:
    :return seconds:

    """
    if time_string is None:
        raise ParsingError("time_string is None")

    values = time_string.split(":")
    if len(values) > 1:
        return colon_separated_time_string_to_seconds(values)

    try:
        m = float(values[0])
        return 60 * m
    except ValueError:
        if re.search(r"\d+h", values[0]):
            return 60 * 60 * float(values[0][:-1])
        elif re.search(r"\d+s", values[0]):
            return float(values[0][:-1])
        else:
            raise ParsingError(f"unknown time format: {time_string}")


def colon_separated_time_string_to_seconds(values: list[str]) -> float:
    # format HH:MM:SS
    if len(values) == 3:
        try:
            h = float(values[0])
            m = float(values[1])
            s = float(values[2])
        except ValueError:
            raise ParsingError("colon time format error")
        else:
            return h * 60 * 60 + m * 60 + s
    # format MM:SS
    elif len(values) == 2:
        try:
            m = float(values[0])
            s = float(values[1])
        except ValueError:
            raise ParsingError("colon time format error")
        else:
            return m * 60 + s
    else:
        raise ParsingError("colon time format error")


def parse_military_time_string(time_string: str) -> datetime.time:
    # e.g. 1600 for 16:00
    if len(time_string) != 4:
        raise ParsingError(f"incorrect military time {time_string}")
    try:
        hour = int(time_string[0:2])
        minutes = int(time_string[2:])
    except ValueError:
        raise ParsingError(f"incorrect military time {time_string}")
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
    reg = re.search("[0-2][0-9][0-5][0-9]-[0-2][0-9][0-5][0-9]", time_string)
    if reg is None:
        raise ParsingError("wrong time format")
    s, e = reg.group().split("-")

    start_t = parse_military_time_string(s)
    end_t = parse_military_time_string(e)
    return start_t, end_t


def get_bushido_date_from_datetime(
    dt: datetime.datetime, tz: datetime.tzinfo, start_hour: int
) -> datetime.date:
    local_dt = dt.astimezone(tz)
    if 0 <= local_dt.hour < start_hour:
        return local_dt.date() - datetime.timedelta(days=1)
    else:
        return local_dt.date()


def find_previous_sunday(dt: datetime.date) -> datetime.date:
    """
    Finds the previous Sunday of the given date
    e.g., input: 01.01.2020
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


def parse_datetime(value: str) -> datetime.datetime:
    return datetime.datetime.strptime(value, "%Y%m%d-%H%M").replace(tzinfo=datetime.UTC)
