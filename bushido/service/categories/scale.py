# project imports
from bushido.exceptions import ValidationError
from bushido.data.categories.scale import ScaleModel, ScaleRepository
from bushido.service.log import AbsLogService


class LogService(AbsLogService):
    def __init__(self, repo: ScaleRepository):
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

        keiko = ScaleModel(weight=weight, belly=belly)
        return keiko
