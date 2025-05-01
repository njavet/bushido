from sqlalchemy.orm import Session

# project imports
from bushido.exceptions import ValidationError
from bushido.data.categories.lifting import KeikoModel, Repository


class UnitService:
    def __init__(self, repo):
        self.repo = repo

    @classmethod
    def from_session(cls, session: Session):
        return cls(Repository(session))

    def get_units(self) -> list:
        units = self.repo.get_units()
        lst = []
        for unit in units:
            t = T(date=get_bushido_date_from_timestamp(unit.timestamp),
                  round=unit.round_nr,
                  breaths=unit.breaths,
                  retention=unit.retention)
            lst.append(t)
        return lst



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
