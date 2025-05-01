from collections import defaultdict
import datetime
import pytz

# project imports
from bushido.conf import DAY_START_HOUR, LOCAL_TIME_ZONE

def get_days() -> dict:
    days = {}
    start = datetime.date(2023, 1, 1)
    while start <= datetime.date.today():
        days[start] = []
        start = start + datetime.timedelta(days=1)
    return days


def get_weeks(days) -> dict:
    week = 0
    weeks = defaultdict(dict)
    start = datetime.date(2023, 1, 1)
    day = 1
    while start <= datetime.date.today():
        weeks[week][start] = days[start]
        if day % 7 == 0:
            week += 1
        day += 1
        start = start + datetime.timedelta(days=1)
    return weeks


def get_datetime_from_timestamp(timestamp: int,
                                timezone='Europe/Zurich') -> datetime.datetime:
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
