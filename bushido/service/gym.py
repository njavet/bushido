import datetime

# project imports
from bushido.service.base import AbsUnitParser
from bushido.model.gym import GymUnit
from bushido.utils.parsing import parse_start_end_time_string


class UnitParser(AbsUnitParser):
    def __init__(self):
        super().__init__()

    def parse_unit(self, emoji, words, comment):
        today = datetime.date.today()
        start_t, end_t = parse_start_end_time_string(words[0])
        start_dt = datetime.datetime(today.year,
                                     today.month,
                                     today.day,
                                     start_t.hour,
                                     start_t.minute)
        end_dt = datetime.datetime(today.year,
                                   today.month,
                                   today.day,
                                   end_t.hour,
                                   end_t.minute)
        try:
            gym = words[1]
        except IndexError:
            raise ValueError('no gym')

        gym_unit = GymUnit(emoji=emoji,
                           start_t=start_t,
                           end_t=end_t,
                           gym=gym,
                           comment=comment)
        return gym_unit
