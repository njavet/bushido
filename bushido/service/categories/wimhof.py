from sqlalchemy.orm import Session

# project imports
from bushido.exceptions import ValidationError
from bushido.utils.dtf import get_bushido_date_from_timestamp
from bushido.data.categories.wimhof import KeikoModel, Repository


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
            dix = {'date': get_bushido_date_from_timestamp(unit.timestamp),
                   'round': unit.round_nr,
                   'breaths': unit.breaths,
                   'retention': unit.retention}
            lst.append(dix)
        return lst


def create_keiko(words):
    try:
        breaths = [int(bs) for bs in words[::2]]
        retentions = [int(r) for r in words[1::2]]
    except ValueError:
        raise ValidationError('invalid input')

    if len(breaths) != len(retentions):
        raise ValidationError(
            'Not the same number of breaths and retentions'
        )
    if len(retentions) < 1:
        raise ValidationError('No round')

    keikos = []
    for i, (b, r) in enumerate(zip(breaths, retentions)):
        keiko = KeikoModel(round_nr=i,
                           breaths=b,
                           retention=r)
        keikos.append(keiko)

    return keikos
