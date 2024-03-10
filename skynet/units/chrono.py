# general imports
import peewee as pw
import config
import collections

# project imports
import unit
import db


class UnitProcessor(unit.UnitProcessor):
    def __init__(self, module_name, unit_name, emoji):
        super().__init__(module_name, unit_name, emoji)

    def subunit_handler(self, words):
        pass

    @classmethod
    def parse_words(cls, words):
        pass


class ModuleStats(unit.ModuleStats):
    def __init__(self, unit_names):
        super().__init__(unit_names)
        self.subunit_model = Chrono


class Chrono(db.SubUnit):
    seconds = pw.FloatField()


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([Chrono], safe=True)
database.close()
