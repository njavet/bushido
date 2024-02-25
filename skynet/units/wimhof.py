# general imports
import collections
import peewee as pw

# project imports
import db
import config
import unitproc
from utils import exceptions


class UnitProcessor(unitproc.UnitProcessor):
    def __init__(self):
        super().__init__()
        self.unit_model = WimhofUnit


class Unit(unitproc.Unit):
    def __init__(self):
        super().__init__()
        self.unit_retriever = UnitRetriever()


class UnitRetriever(unitproc.UnitRetriever):
    def __init__(self):
        super().__init__()
        self.unit_model = WimhofUnit
        self.subunit_model = WimhofRound

    def datetime2unit(self, user_id):
        query = self.retrieve_units(user_id)
        dt2units = collections.defaultdict(list)
        for unit in query:
            dt2units[unit.log_time].append(unit.wimhofround)
        return dt2units

    def date2unit_str(self, user_id):
        date2units = self.date2units(user_id)
        dix = collections.defaultdict(str)
        for k, v in date2units.items():
            dix[k] = v[0].unit_emoji
        return dix


class WimhofUnit(db.Unit):

    def parse(self, words):
        breaths = [int(b) for b in words[::2]]
        retentions = [int(r) for r in words[1::2]]
        if len(breaths) != len(retentions):
            raise exceptions.UnitProcessingError('Not the same number of breaths and seconds')
        if len(breaths) < 1:
            raise exceptions.UnitProcessingError('At least one round necessary')
        self.save()

        for i, (b, r) in enumerate(zip(breaths, retentions)):
            r = WimhofRound(unit=self.id,
                            round_nr=i,
                            breaths=b,
                            retention=r)
            r.save()


class WimhofRound(db.SubUnit):
    round_nr = pw.IntegerField()
    breaths = pw.IntegerField()
    retention = pw.IntegerField()
    unit = pw.ForeignKeyField(WimhofUnit, backref='')

    def __str__(self):
        return 'Breaths: {}, Retention: {}'.format(self.breaths, self.retention)


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([WimhofUnit, WimhofRound], safe=True)
database.close()
