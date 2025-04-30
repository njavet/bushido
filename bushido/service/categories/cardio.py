# project imports
from bushido.exceptions import ValidationError
from bushido.utils.parsing import (parse_military_time_string,
                                   parse_time_string)
from bushido.data.repo import Repository
from bushido.data.categories.cardio import KeikoModel
from bushido.service.unit import BaseUnitService


class UnitService(BaseUnitService):
    def __init__(self, repo: Repository):
        super().__init__(repo)

    def create_keiko(self, words):
        start_t = parse_military_time_string(words[0])
        seconds = parse_time_string(words[1])
        try:
            gym = words[2]
        except IndexError:
            raise ValidationError('no gym')

        try:
            distance = float(words[3])
        except (ValueError, IndexError):
            distance = None

        keiko = KeikoModel(start_t=start_t,
                           seconds=seconds,
                           gym=gym,
                           distance=distance)
        return keiko
