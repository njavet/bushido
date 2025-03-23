from zoneinfo import ZoneInfo
import datetime

# project imports
from bushido.service.categories.category import AbsUnitParser, AbsUnitProcessor
from bushido.model.gym import GymUnit
from bushido.utils.parsing import parse_start_end_time_string
from bushido.data.categories.gym import Uploader


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine):
        super().__init__(engine)
        self.parser = UnitParser()
        self.uploader = Uploader(engine)

    def process_unit(self, emoji, words, comment):
        gym_unit = self.parser.parse_unit(emoji, words, comment)
        pass


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
            raise ValueError('no gym')

        gym_unit = GymUnit(emoji=emoji,
                           start_t=start_ts,
                           end_t=end_ts,
                           gym=gym,
                           comment=comment)
        return gym_unit
