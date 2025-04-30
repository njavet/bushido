# project imports
from bushido.exceptions import ValidationError
from bushido.data.categories.wimhof import KeikoModel, Repository
from bushido.service.unit import AbsUnitService


class UnitService(AbsUnitService):
    def __init__(self, repo: Repository):
        super().__init__(repo)

    def create_keiko(self, words):
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
