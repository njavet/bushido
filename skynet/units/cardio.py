# general imports
import collections

import peewee as pw
import datetime
import re

# project imports
import config
import unitproc
import db
from utils import exceptions


class UnitProcessor(unitproc.UnitProcessor):
    def __init__(self):
        super().__init__()
        self.unit_model = CardioUnit


class Unit(unitproc.Unit):
    def __init__(self):
        super().__init__()
        self.unit_retriever = UnitRetriever()


class UnitRetriever(unitproc.UnitRetriever):
    def __init__(self):
        super().__init__()
        self.unit_model = CardioUnit


class CardioUnit(db.ChronoUnit):
    gym = pw.CharField()
    distance = pw.FloatField(null=True)
    avghr = pw.IntegerField(null=True)
    maxhr = pw.IntegerField(null=True)
    cal = pw.IntegerField(null=True)
    avg_speed = pw.FloatField(null=True)

    def parse(self, words):
        try:
            sh, sm = self.parse_military_time(words[0])
            self.start = self.log_time.replace(hour=sh, minute=sm)
        except IndexError:
            raise exceptions.UnitProcessingError('CardioUnit: No start')
        except exceptions.UnitProcessingError:
            raise

        try:
            self.parse_min_sec_str(words[1])
        except IndexError:
            raise exceptions.UnitProcessingError('CardioUnit: No time')
        except exceptions.UnitProcessingError:
            raise

        try:
            self.gym = words[2]
        except IndexError:
            raise exceptions.UnitProcessingError('CardioUnit: No gym')

        try:
            self.distance = float(words[3])
            self.avg_speed = (1000 * self.distance) / self.seconds
        except IndexError:
            pass
        except ValueError:
            raise exceptions.UnitProcessingError('CardioUnit: wrong distance format')
        try:
            self.avghr = float(words[4])
        except IndexError:
            pass
        except ValueError:
            raise exceptions.UnitProcessingError('CardioUnit: wrong avg hr format')
        try:
            self.maxhr = float(words[5])
        except IndexError:
            pass
        except ValueError:
            raise exceptions.UnitProcessingError('CardioUnit: wrong max hr format')
        try:
            self.cal = float(words[6])
        except IndexError:
            pass
        except ValueError:
            raise exceptions.UnitProcessingError('CardioUnit: wrong cal format')

    def seconds2time_str(self):
        m, s = divmod(self.seconds, 60)
        return str(m).zfill(2) + ':' + str(s).zfill(2)

    def __str__(self):
        return ', '.join([self.seconds2time_str(),
                          str(self.distance),
                          '{:0.1f}'.format(self.avg_speed),
                          str(self.avghr),
                          str(self.maxhr),
                          str(self.cal)])


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([CardioUnit], safe=True)
database.close()

