# general imports
import collections

# project imports
import unit
import db


class UnitProcessor(unit.UnitProcessor):
    def __init__(self, unit_emoji, unit_name):
        super().__init__(unit_emoji, unit_name)
        self.unit_model = db.ChronoUnit


class UnitStats(unit.UnitStats):
    def __init__(self):
        super().__init__()
        self.unit_model = db.ChronoUnit

    def date2unit_str(self, user_id):
        date2units = self.date2units(user_id)
        dix = collections.defaultdict(str)
        for k, v in date2units.items():
            dix[k] = ' '.join([str(u) for u in v])
        return dix





