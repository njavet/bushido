# general imports
import peewee as pw
import collections
import operator

# project imports
import config
import db
from utils import exceptions, utilities
import unit


class UnitProcessor(unit.UnitProcessor):
    def __init__(self, unit_emoji, unit_name):
        super().__init__(unit_emoji, unit_name)
        self.unit_model = ResistanceUnit


class UnitStats(unit.UnitStats):
    def __init__(self):
        super().__init__()
        self.unit_model = ResistanceUnit
        self.subunit_model = ResistanceSet

    def datetime2unit(self, user_id):
        query = self.retrieve_units(user_id)
        dix = collections.defaultdict(dict)
        for u in query:
            dix[u.unit_name] = collections.defaultdict(list)
        for u in query:
            dix[u.unit_name][u.log_time].append(u.resistanceset)
        return dix

    def date2unit_str(self, user_id):
        date2units = self.date2units(user_id)
        dix = collections.defaultdict(str)
        for k, v in date2units.items():
            dix[k] = ' '.join([str(u.unit_emoji) for u in v])
        return dix

    def get_heaviest(self, units):

        return sorted(units, key=lambda u: (u.resistanceset.weight,
                                                     u.resistanceset.reps),
                               reverse=True)

    def get_most_reps(self, units):
        return sorted(units, key=lambda u: (u.resistanceset.reps,
                                                      u.resistanceset.weight),
                                reverse=True)

    def get_best_orm(self, units):
        return sorted(units, key=lambda u: (u.resistanceset.orm,
                                                     -u.resistanceset.reps,
                                                     u.resistanceset.weight),
                               reverse=True)

    def get_best_rs(self, units):
        return sorted(units, key=lambda u: (u.resistanceset.rel_strength,
                                                    u.resistanceset.weight,
                                                    u.resistanceset.reps),
                              reverse=True)

    def compute_stats(self, units):
        self.heaviest = units[0]
        self.most_reps = units[0]
        self.best_orm = units[0]
        self.best_rs = units[0]
        for unit in units:
            if unit.resistanceset.weight > self.heaviest.resistanceset.weight:
                self.heaviest = unit
            if unit.resistanceset.weight == self.heaviest.resistanceset.weight:
                if unit.resistanceset.reps > self.heaviest.resistanceset.reps:
                    self.heaviest = unit
            if unit.resistanceset.reps > self.most_reps.resistanceset.reps:
                self.most_reps = unit
            if unit.resistanceset.reps == self.most_reps.resistanceset.reps:
                if unit.resistanceset.weight > self.most_reps.resistanceset.weight:
                    self.most_reps = unit
            if unit.resistanceset.orm > self.best_orm.resistanceset.orm:
                self.best_orm = unit
            if unit.resistanceset.rel_strength > self.best_rs.resistanceset.rel_strength:
                self.best_rs = unit


class ResistanceUnit(db.Unit):
    unit_name = pw.CharField()

    def parse(self, words):
        try:
            weights = [float(w) for w in words[::3]]
            reps = [float(r) for r in words[1::3]]
            pauses = [float(p) for p in words[2::3]] + [0]
        except ValueError:
            raise exceptions.UnitProcessingError('invalid input')

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

    def __str__(self):
        return 'Weight: {}, Reps: {}, Pause: {}'.format(self.weight, self.reps, self.pause)


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([ResistanceUnit, ResistanceSet], safe=True)
database.close()


