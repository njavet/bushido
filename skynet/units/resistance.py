# general imports
import peewee as pw

# project imports
import config
import db
from utils import exceptions, utilities
import unitproc


class UnitProcessor(unitproc.UnitProcessor):
    def __init__(self):
        super().__init__()
        self.unit_model = ResistanceUnit


class UnitRetriever(unitproc.UnitRetriever):
    def __init__(self):
        super().__init__()
        self.unit_model = ResistanceUnit
        self.subunit_model = ResistanceSet


class ResistanceUnit(db.Unit):
    unit_name = pw.CharField()

    def parse(self, words):
        weights = [float(w) for w in words[::3]]
        reps = [float(r) for r in words[1::3]]
        pauses = [float(p) for p in words[2::3]] + [0]

        if len(reps) != len(weights):
            raise exceptions.UnitProcessingError('Not the same number of reps and weights')
        if len(pauses) != len(reps):
            raise exceptions.UnitProcessingError('break error')
        if len(reps) < 1:
            raise exceptions.UnitProcessingError('No set')

        at = db.User.select().where(db.User.user_id == self.user_id).get()
        self.save()

        for i, (w, r, b) in enumerate(zip(weights, reps, pauses)):
            orm = utilities.estimate_orm(w, r)
            try:
                rel_strength = orm / at.weight
            except TypeError:
                rel_strength = None
            ls = ResistanceSet(unit=self.id,
                               set_nr=i,
                               weight=w,
                               reps=r,
                               pause=b,
                               orm=orm,
                               rel_strength=rel_strength)
            ls.save()


class ResistanceSet(db.SubUnit):
    set_nr = pw.IntegerField()
    weight = pw.FloatField()
    reps = pw.FloatField()
    pause = pw.IntegerField()
    orm = pw.FloatField()
    rel_strength = pw.FloatField(null=True)
    unit = pw.ForeignKeyField(ResistanceUnit, backref='')


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([ResistanceUnit, ResistanceSet], safe=True)
database.close()
