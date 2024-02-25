# general imports
import collections

import peewee as pw

# project imports
import config
import db
import unitproc
from utils import exceptions


class UnitProcessor(unitproc.UnitProcessor):
    def __init__(self):
        super().__init__()
        self.unit_model = BalanceUnit

    def post_saving(self, user_id):
        user = db.User.select().where(db.User.user_id == user_id).get()
        user.weight = self.unit.weight
        user.save()


class Unit(unitproc.Unit):
    def __init__(self):
        super().__init__()
        self.unit_retriever = UnitRetriever()


class UnitRetriever(unitproc.UnitRetriever):
    def __init__(self):
        super().__init__()
        self.unit_model = BalanceUnit

    def datetime2unit(self, user_id):
        query = self.retrieve_units(user_id)
        return {unit.log_time: unit for unit in query}

    def date2unit_str(self, user_id):
        date2units = self.date2units(user_id)
        dix = collections.defaultdict(str)
        for k, v in date2units.items():
            dix[k] = str(v[0])
        return dix


class BalanceUnit(db.Unit):
    weight = pw.FloatField()
    fat = pw.FloatField(null=True)
    water = pw.FloatField(null=True)
    muscles = pw.FloatField(null=True)

    def parse(self, words):
        try:
            self.weight = float(words[0])
        except (IndexError, ValueError):
            raise exceptions.UnitProcessingError('Specify the weight')
        try:
            self.fat = float(words[1])
        except (IndexError, ValueError):
            self.fat = None
        try:
            self.water = float(words[2])
        except (IndexError, ValueError):
            self.water = None
        try:
            self.muscles = float(words[3])
        except (IndexError, ValueError):
            self.muscles = None

    def __str__(self):
        return self.unit_emoji + '  ' + str(self.weight) + 'Kg'


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([BalanceUnit], safe=True)
database.close()
