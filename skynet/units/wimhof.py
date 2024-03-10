# general imports
import collections
import peewee as pw

# project imports
import db
import config
import unit
from utils import exceptions


class UnitProcessor(unit.UnitProcessor):
    def __init__(self, module_name, unit_name, emoji):
        super().__init__(module_name, unit_name, emoji)

    def subunit_handler(self, words):
        attributes = self.parse_words(words)
        for round_nr, attrs in attributes.items():
            Wimhof.create(unit_id=self.unit.id, round_nr=round_nr, **attrs)

    @classmethod
    def parse_words(cls, words):
        try:
            breaths = [int(b) for b in words[::2]]
            retentions = [int(r) for r in words[1::2]]
        except ValueError:
            raise exceptions.UnitProcessingError('value error')
        if len(breaths) != len(retentions):
            raise exceptions.UnitProcessingError('Not the same number of breaths and seconds')
        if len(breaths) < 1:
            raise exceptions.UnitProcessingError('At least one round necessary')

        attributes = {}
        for round_nr, (b, r) in enumerate(zip(breaths, retentions)):
            attributes[round_nr] = {'breaths': b, 'retention': r}
        return attributes


class ModuleStats(unit.ModuleStats):
    def __init__(self, unit_names):
        super().__init__(unit_names)
        self.subunit_model = Wimhof

    def datetime2unit(self, user_id):
        query = self.retrieve_units(user_id)
        dt2units = collections.defaultdict(list)
        for unit in query:
            dt2units[unit.log_time].append(unit.wimhof)
        return dt2units

    def date2unit_str(self, user_id):
        date2units = self.date2units(user_id)
        dix = collections.defaultdict(str)
        for k, v in date2units.items():
            dix[k] = v[0].unit_emoji
        return dix


class Wimhof(db.SubUnit):
    round_nr = pw.IntegerField()
    breaths = pw.IntegerField()
    retention = pw.IntegerField()


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([Wimhof], safe=True)
database.close()
