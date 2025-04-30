# project imports
from bushido.utils.parsing import parse_time_string
from bushido.data.categories.chrono import ChronoModel, ChronoRepository
from bushido.service.log import AbsLogService


class LogService(AbsLogService):
    def __init__(self, repo: ChronoRepository):
        super().__init__(repo)

    def create_keiko(self, words):
        seconds = parse_time_string(words[0])
        keiko = ChronoModel(seconds=seconds)
        return keiko
