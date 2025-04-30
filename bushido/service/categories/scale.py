# project imports
from bushido.exceptions import ValidationError
from bushido.data.categories.scale import KeikoModel, Repository
from bushido.service.unit import AbsUnitService


class UnitService(AbsUnitService):
    def __init__(self, repo: Repository):
        super().__init__(repo)

    def create_keiko(self, words):
        try:
            weight = float(words[0])
        except (IndexError, ValueError):
            raise ValidationError('wrong format')

        try:
            belly = float(words[1])
        except ValueError:
            raise ValidationError('wrong belly format')
        except IndexError:
            belly = None

        keiko = KeikoModel(weight=weight, belly=belly)
        return keiko
