# general imports
import datetime
import peewee as pw
import re

# project imports
import config
from utils import exceptions


class BaseModel(pw.Model):
    class Meta:
        database = pw.SqliteDatabase(config.db_name)


class User(BaseModel):
    user_id = pw.IntegerField(primary_key=True)
    user_name = pw.CharField(default='Platon')
    age = pw.IntegerField(null=True)
    weight = pw.FloatField(null=True)
    height = pw.FloatField(null=True)


class Unit(BaseModel):
    user = pw.ForeignKeyField(User)
    unit_emoji = pw.CharField()
    log_time = pw.DateTimeField()
    # a unit that is logged after midnight before sleeping
    # should count for the last day 0400-0359 is the day then
    log_date = pw.DateField()
    comment = pw.TextField(null=True)

    def set_time(self, recv_time):
        if recv_time is None:
            self.log_time = datetime.datetime.now()
        else:
            self.log_time = recv_time

        if datetime.time(0) < self.log_time.time() < datetime.time(3):
            # should count for the last day
            self.log_date = self.log_time.date() - datetime.timedelta(days=1)
        else:
            self.log_date = self.log_time.date()

    def parse(self, words):
        raise NotImplementedError


class SubUnit(BaseModel):
    unit = pw.ForeignKeyField(Unit)


class ChronoUnit(Unit):
    seconds = pw.FloatField()
    start = pw.DateTimeField(null=True)
    end = pw.DateTimeField(null=True)
    place = pw.CharField(null=True)
    topic = pw.CharField(null=True)
    effort = pw.IntegerField(default=3)

    def parse(self, words):
        try:
            self.parse_and_set_time_string(words[0])
        except IndexError:
            raise exceptions.UnitProcessingError('Specify the Time')

    def parse_and_set_time_string(self, min_sec_str):
        try:
            min_sec = min_sec_str.split(':')
            self.seconds = float(min_sec[0]) * 60
            self.seconds += float(min_sec[1])
        except ValueError:
            raise exceptions.UnitProcessingError('Time format error')
        except IndexError:
            pass

    @staticmethod
    def parse_military_time(military_time_str):
        # e.g. 1600 for 16:00
        if len(military_time_str) != 4:
            raise exceptions.UnitProcessingError('incorrect military time')
        try:
            hour = int(military_time_str[0:2])
            minute = int(military_time_str[2:])
        except ValueError:
            raise exceptions.UnitProcessingError('incorrect military time')
        else:
            return hour, minute

    def parse_and_set_start_end_time(self, time_str):
        """
            the format is HHMM-HHMM as start time and end time
        :param time_str:
        :return:
        """
        reg = re.search('[0-2][0-9][0-5][0-9]-[0-2][0-9][0-5][0-9]', time_str)
        try:
            s, e = reg.group().split('-')
        except AttributeError:
            raise exceptions.UnitProcessingError('wrong time format')
        # if we are here we know that we have s = 'HHMM' and e = 'HHMM'
        sh, sm = self.parse_military_time(s)
        eh, em = self.parse_military_time(e)
        self.start = self.log_time.replace(hour=sh, minute=sm)
        self.end = self.log_time.replace(hour=eh, minute=em)

        # TODO error: end time is after log time
        # receive time is "right after training" aka a few minutes after the end
        # "normal case": 0400 <= start < end <= 2359


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([User, ChronoUnit], safe=True)
database.close()
