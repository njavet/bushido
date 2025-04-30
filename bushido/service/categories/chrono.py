# project imports
from bushido.utils.parsing import parse_time_string
from bushido.data.repo import Repository
from bushido.data.categories.chrono import KeikoModel
from bushido.service.unit import BaseUnitService


class UnitService(BaseUnitService):
    def __init__(self, repo: Repository):
        super().__init__(repo)

    def create_keiko(self, words):
        seconds = parse_time_string(words[0])
        keiko = KeikoModel(seconds=seconds)
        return keiko
