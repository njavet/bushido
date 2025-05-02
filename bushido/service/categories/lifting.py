from collections import defaultdict
from sqlalchemy.orm import Session

# project imports
from bushido.exceptions import ValidationError
from bushido.utils.dtf import get_bushido_date_from_timestamp
from bushido.data.categories.lifting import KeikoModel, Repository


class UnitService:
    def __init__(self, repo):
        self.repo = repo

    @classmethod
    def from_session(cls, session: Session):
        return cls(Repository(session))

    def get_sets(self) -> list:
        units = self.repo.get_sets()
        lst = []
        for unit in units:
            dix = {'unit_name': unit.unit_name,
                   'date': get_bushido_date_from_timestamp(unit.timestamp),
                   'set': unit.set_nr,
                   'weight': unit.weight,
                   'reps': unit.reps,
                   'pause': unit.pause}
            lst.append(dix)
        return lst

    def get_unit_name_sets(self):
        units = self.repo.get_sets()
        dix = defaultdict(list)
        for unit in units:
            dix[unit.unit_name].append(unit)
        return dix

    def get_lifting_sessions(self):
        dix = self.get_unit_name_sets()
        res = {}
        for unit_name, sets in dix.items():
            res[unit_name] = defaultdict(list)
            for s in sets:
                res[unit_name][s.timestamp].append(s)
        return res

    def completed_5x5(self, sets):
        if len(sets) != 5:
            return False

        for s in sets:
            if s.reps != 5:
                return False
        return True

    def get_avg_weight_reps(self, sets):
        w = sum([s.weight for s in sets]) / len(sets)
        r = sum([s.reps for s in sets]) / len(sets)
        return w, r

    def get_completed_5x5(self):
        dix = self.get_lifting_sessions()
        res = defaultdict(list)
        for unit_name, sessions in dix.items():
            for ts, sets in sessions.items():
                if self.completed_5x5(sets):
                    w, r = self.get_avg_weight_reps(sets)
                    res[unit_name].append((get_bushido_date_from_timestamp(ts), w, r))
        return res


def create_keiko(words):
    try:
        weights = [float(w) for w in words[::3]]
        reps = [float(r) for r in words[1::3]]
        pauses = [int(p) for p in words[2::3]] + [0]
    except ValueError:
        raise ValidationError('invalid input')

    if len(reps) < 1:
        raise ValidationError('No set')
    if len(reps) != len(weights):
        raise ValidationError(
            'Not the same number of reps and weights')
    if len(pauses) != len(reps):
        raise ValidationError('break error')

    keikos = []
    for i, (w, r, p) in enumerate(zip(weights, reps, pauses)):
        keiko = KeikoModel(set_nr=i,
                           weight=w,
                           reps=r,
                           pause=p)
        keikos.append(keiko)

    return keikos
