# general imports
import collections
import peewee as pw

# project imports
import unit
import parsing
from utils import exceptions
import config
import db


class UnitProcessor(unit.UnitProcessor):
    def __init__(self, module_name, unit_name, emoji):
        super().__init__(module_name, unit_name, emoji)

    def subunit_handler(self, words):
        self.subunit = Gym(**self.parse_words(words))
        self.subunit.unit_id = self.unit.id
        self.subunit.save()

    @classmethod
    def parse_words(cls, words):
        start_t, end_t = parsing.parse_start_end_time_string(words[0])
        return {'start_t': start_t, 'end_t': end_t, 'gym': words[1]}


class ModuleStats(unit.ModuleStats):
    def __init__(self, unit_names):
        super().__init__(unit_names)
        self.subunit_model = Gym

    def datetime2unit(self, user_id):
        query = self.retrieve_units(user_id)
        dix = collections.defaultdict(dict)
        for u in query:
            dix[u.unit_name][u.log_time] = u
        return dix

    def date2unit_str(self, user_id):
        date2units = self.date2units(user_id)
        dix = collections.defaultdict(str)
        for k, v in date2units.items():
            dix[k] = v[0].unit_emoji
        return dix


class Gym(db.SubUnit):
    start_t = pw.TimeField()
    end_t = pw.TimeField()
    gym = pw.CharField()
    training = pw.CharField(null=True)


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([Gym], safe=True)
database.close()
