# project imports
from bushido.exceptions import ValidationError
from bushido.data.categories.wimhof import KeikoModel
from bushido.schema.res import UnitResponse
from bushido.service.unit import BaseUnitService


class UnitService(BaseUnitService):
    def __init__(self, repo):
        super().__init__(repo)

    def get_units(self,
                  unit_name=None,
                  start_t=None,
                  end_t=None) -> list[UnitResponse]:
        return self._get_units(unit_name, start_t, end_t, KeikoModel)


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
