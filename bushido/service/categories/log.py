# project imports
from bushido.data.categories.log import LogModel, LogRepository
from bushido.service.log import AbsLogService


class LogService(AbsLogService):
    def __init__(self, repo: LogRepository):
        super().__init__(repo)

    def create_keiko(self, words):
        try:
            log = words[0]
        except IndexError:
            log = None

        keiko = LogModel(log=log)
        return keiko
