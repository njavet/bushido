# general imports
import collections
import peewee as pw

# project imports
import config
import db
import unit
from utils import exceptions


class UnitProcessor(unit.UnitProcessor):
    def __init__(self, module_name, unit_name, emoji):
        super().__init__(module_name, unit_name, emoji)

    def subunit_handler(self, words):
        self.subunit = Balance(**self.parse_words(words))
        self.subunit.unit_id = self.unit.id
        self.subunit.save()

    @classmethod
    def parse_words(cls, words: list) -> dict:
        try:
            attributes = {'weight': float(words[0])}
        except (IndexError, ValueError):
            raise exceptions.UnitProcessingError('Specify the weight')

        try:
            attributes['fat'] = float(words[1])
        except (IndexError, ValueError):
            attributes['fat'] = None

        try:
            attributes['water'] = float(words[2])
        except (IndexError, ValueError):
            attributes['water'] = None

        try:
            attributes['muscles'] = float(words[3])
        except (IndexError, ValueError):
            attributes['muscles'] = None

        return attributes

    def post_saving(self, user_id):
        user = db.User.select().where(db.User.user_id == user_id).get()
        user.weight = self.subunit.weight
        user.save()


class ModuleStats(unit.ModuleStats):
    def __init__(self, unit_names):
        super().__init__(unit_names)
        self.subunit_model = Balance


class Balance(db.SubUnit):
    weight = pw.FloatField()
    fat = pw.FloatField(null=True)
    water = pw.FloatField(null=True)
    muscles = pw.FloatField(null=True)


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([Balance], safe=True)
database.close()
