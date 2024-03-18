# general imports
import datetime

import peewee as pw
import collections
import operator

# project imports
import config
import db
from utils import exceptions, utilities
import unit
from units.balance import Balance


class UnitProcessor(unit.UnitProcessor):
    def __init__(self, module_name, unit_name, emoji):
        super().__init__(module_name, unit_name, emoji)

    def subunit_handler(self, words):
        attributes = self.parse_words(words)
        for set_nr, attrs in attributes.items():
            Lifting.create(unit_id=self.unit.id,
                           set_nr=set_nr,
                           weight=attrs['weight'],
                           reps=attrs['reps'],
                           pause=attrs['pause'])

    @classmethod
    def parse_words(cls, words):
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

        attributes = {}
        for i, (weight, reps, pause) in enumerate(zip(weights, reps, pauses)):
            attributes[i] = {'weight': weight, 'reps': reps, 'pause': pause}
        return attributes


class ModuleStats(unit.ModuleStats):
    def __init__(self, unit_names):
        super().__init__(unit_names)
        self.subunit_model = Lifting

    def datetime2unit(self, user_id):
        query = self.retrieve_units(user_id)
        dix = collections.defaultdict(dict)
        for u in query:
            dix[u.unit_name] = collections.defaultdict(list)
        for u in query:
            dix[u.unit_name][u.log_time].append(u.lifting)
        return dix

    def date2unit_str(self, user_id):
        date2units = self.date2units(user_id)
        dix = collections.defaultdict(str)
        for k, v in date2units.items():
            dix[k] = ' '.join([str(u.unit_emoji) for u in v])
        return dix

    def unit_name2unit_list(self, user_id):
        columns = ['Date', 'Time', 'BW', 'Set_Nr', 'Weight', 'Reps']
        dix = {unit_name: [columns] for unit_name in self.unit_names}
        #query = self.retrieve_units(user_id)

        sq0 = (db.Unit
               .select(db.Unit.log_date,
                       db.Unit.log_time,
                       db.Unit.unit_emoji,
                       Balance.weight)
               .join(Balance)
               .group_by(db.Unit.log_date)
               .alias('balance_units')
               )

        query = (db.Unit
                 .select(db.Unit,
                         Lifting,
                         sq0.c.weight.alias('bw'),
                         sq0.c.unit_emoji.alias('balance_emoji'),
                         sq0.c.log_time)
                 .join(Lifting)
                 .switch(db.Unit)
                 .join(sq0, pw.JOIN.LEFT_OUTER, on=(db.Unit.log_date == sq0.c.log_date))
                 .order_by(db.Unit.log_time.desc())
                 )

        for u in query:
            date = datetime.datetime.strftime(u.log_time, '%d.%m.%y')
            time = datetime.datetime.strftime(u.log_time, '%H:%M')
            try:
                bw = u.unit.balance_emoji + '  ' + str(u.unit.bw) + 'Kg'
            except AttributeError:
                bw = ''

            row = [date,
                   time,
                   bw,
                   u.lifting.set_nr,
                   u.lifting.weight,
                   u.lifting.reps]
            dix[u.unit_name].append(row)
        return dix


class Lifting(db.SubUnit):
    set_nr = pw.IntegerField()
    weight = pw.FloatField()
    reps = pw.FloatField()
    pause = pw.IntegerField()

    def __str__(self):
        return ' '.join([str(self.weight), str(self.reps), str(self.pause)])


database = pw.SqliteDatabase(config.db_name)
database.connect()
database.create_tables([Lifting], safe=True)
database.close()
