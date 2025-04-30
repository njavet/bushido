# project imports
from bushido.utils.parsing import parse_time_string
from bushido.data.categories.chrono import KeikoModel, Repository
from bushido.service.unit import AbsUnitService


class UnitService(AbsUnitService):
    def __init__(self, repo: Repository):
        super().__init__(repo)

    def create_keiko(self, words):
        seconds = parse_time_string(words[0])
        keiko = KeikoModel(seconds=seconds)
        return keiko
