from bushido.exceptions import ValidationError
from bushido.data.categories.lifting import KeikoModel, Repository
from bushido.service.unit import AbsUnitService


class UnitService(AbsUnitService):
    def __init__(self, repo: Repository):
        super().__init__(repo)

    def create_keiko(self, words):
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
