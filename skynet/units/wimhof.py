# general imports
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


class UnitRetriever(unitproc.UnitRetriever):
    def __init__(self):
        super().__init__()
        self.unit_model = WimhofUnit
        self.subunit_model = WimhofRound


class WimhofUnit(db.Unit):

    def parse(self, words):
        breaths = [int(b) for b in words[::2]]
        retentions = [float(r) for r in words[1::2]]
        if len(breaths) != len(retentions):
            raise exceptions.UnitProcessingError('Not the same number of breaths and seconds')
        if len(breaths) < 1:
            raise exceptions.UnitProcessingError('At least one round necessary')
        self.save()

        for i, (b, r) in enumerate(zip(breaths, retentions)):
            r = WimhofRound(unit=self.get_id(),
                            round_nr=i,
                            breaths=b,
                            retention=r)
            r.save()


class WimhofRound(db.SubUnit):
    round_nr = pw.IntegerField()
    breaths = pw.IntegerField()
    retention = pw.IntegerField()


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([WimhofUnit, WimhofRound], safe=True)
database.close()
