import datetime
import pytz

from bushido.conf import day_start


def get_datetime_from_timestamp(timestamp: int,
                                timezone='Europe/Zurich') -> datetime.datetime:
    cet_timezone = pytz.timezone(timezone)
    cet_dt = datetime.datetime.fromtimestamp(timestamp, cet_timezone)
    return cet_dt


def get_bushido_date_from_datetime(dt: datetime.datetime) -> datetime.date:
    if 0 <= dt.hour < day_start:
        return dt.date() - datetime.timedelta(days=1)
    else:
        return dt.date()


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
