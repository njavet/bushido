# general imports
import collections
import peewee as pw

# project imports
import unit
from utils import exceptions
import config
import db



class UnitProcessor(unit.UnitProcessor):
    def __init__(self):
        super().__init__()
        self.unit_model = MindUnit


class UnitRetriever(unit.UnitRetriever):
    def __init__(self):
        super().__init__()
        self.unit_model = MindUnit

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


class MindUnit(db.ChronoUnit):
    lecture = pw.CharField()
    breaks = pw.IntegerField(null=True)
    efficiency = pw.FloatField(null=True)


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([MindUnit], safe=True)
database.close()
