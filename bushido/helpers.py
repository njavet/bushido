# general imports
import datetime
import os
import re
import pytz

# project imports
import config


def get_data_dir_path() -> str:
    """
        return the absolute path of the data directory
    """
    home = os.path.expanduser('~')
    data_dir_path = os.path.join(home, config.data_dir)
    return data_dir_path


def create_user_data_dir():
    data_dir_path = get_data_dir_path()
    if not os.path.exists(data_dir_path):
        os.makedirs(data_dir_path)


def convert_emoji(emoji):
    try:
        return config.single2double[emoji.encode('utf-8')].decode('utf-8')
    except KeyError:
        return emoji


def get_datetime_from_unix_timestamp(unix_timestamp: float) -> datetime.datetime:
    cet_timezone = pytz.timezone('Europe/Zurich')
    cet_dt = datetime.datetime.fromtimestamp(unix_timestamp, cet_timezone)
    return cet_dt


def get_bushido_date_from_datetime(dt: datetime.datetime) -> datetime.date:
    if 0 <= dt.hour < config.day_start:
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
