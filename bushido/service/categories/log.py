# project imports
from bushido.data.categories.log import KeikoModel, Repository
from bushido.service.unit import AbsUnitService


class UnitService(AbsUnitService):
    def __init__(self, repo: Repository):
        super().__init__(repo)

    def create_keiko(self, words):
        try:
            log = words[0]
        except IndexError:
            log = None

        keiko = KeikoModel(log=log)
        return keiko
