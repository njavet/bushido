# general imports
import collections

import peewee as pw

# project imports
import unitproc
from utils import exceptions
import config
import db


class UnitProcessor(unitproc.UnitProcessor):
    def __init__(self):
        super().__init__()
        self.unit_model = GymUnit


class UnitRetriever(unitproc.UnitRetriever):
    def __init__(self):
        super().__init__()
        self.unit_model = GymUnit

    def datetime2unit(self, user_id):
        query = self.retrieve_units(user_id)
        dix = collections.defaultdict(dict)
        for unit in query:
            dix[unit.unit_name][unit.log_time] = unit
        return dix

    def date2unit_str(self, user_id):
        date2units = self.date2units(user_id)
        dix = collections.defaultdict(str)
        for k, v in date2units.items():
            dix[k] = v[0].unit_emoji
        return dix


class GymUnit(db.ChronoUnit):
    def parse(self, words):
        try:
            self.parse_and_set_start_end_time(words[0])
        except IndexError:
            raise exceptions.UnitProcessingError('Specify the start and end time of the unit!')
        self.seconds = (self.end - self.start).seconds
        try:
            self.place = words[1]
        except IndexError:
            raise exceptions.UnitProcessingError('Specify the gym')

    def __str__(self):
        return 'Training:' + self.unit_name + ' at ' + self.place


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([GymUnit], safe=True)
database.close()
