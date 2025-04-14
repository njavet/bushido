from zoneinfo import ZoneInfo
import datetime

# project imports
from bushido.exceptions import ValidationError
from bushido.utils.parsing import parse_start_end_time_string
from bushido.data.categories.gym import GymModel, GymRepository
from bushido.service.unit import UnitService


class LogService(UnitService):
    def __init__(self, repo: GymRepository):
        super().__init__(repo)

    def create_keiko(self, words):
        today = datetime.date.today()
        start_t, end_t = parse_start_end_time_string(words[0])
        start_dt = datetime.datetime(today.year,
                                     today.month,
                                     today.day,
                                     start_t.hour,
                                     start_t.minute)
        start_dt = start_dt.replace(tzinfo=ZoneInfo('Europe/Zurich'))
        start_ts = int(start_dt.timestamp())

        end_dt = datetime.datetime(today.year,
                                   today.month,
                                   today.day,
                                   end_t.hour,
                                   end_t.minute)
        end_dt = end_dt.replace(tzinfo=ZoneInfo('Europe/Zurich'))
        end_ts = int(end_dt.timestamp())
        try:
            gym = words[1]
        except IndexError:
            raise ValidationError('no gym')

        keiko = GymModel(start_t=start_ts,
                         end_t=end_ts,
                         gym=gym)
        return keiko
