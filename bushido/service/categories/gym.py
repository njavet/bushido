# project imports
from bushido.exceptions import ValidationError
from bushido.utils.parsing import parse_start_end_time_string
from bushido.data.categories.gym import GymModel, GymRepository
from bushido.service.log import AbsLogService


class LogService(AbsLogService):
    def __init__(self, repo: GymRepository):
        super().__init__(repo)

    def create_keiko(self, words):
        start_t, end_t = parse_start_end_time_string(words[0])
        try:
            gym = words[1]
        except IndexError:
            raise ValidationError('no gym')

        keiko = GymModel(start_t=start_t,
                         end_t=end_t,
                         gym=gym)
        return keiko
