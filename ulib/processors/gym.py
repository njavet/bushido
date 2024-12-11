from dataclasses import dataclass, field
from sqlalchemy.orm import Session
import datetime

# project imports
from ulib.processors import AbsUnitProcessor
from ulib.db.models import Gym
from ulib.parsing.parsing import parse_start_end_time_string


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    @dataclass
    class Attrs:
        start_t: float
        end_t: float
        gym: str
        training: str | None = field(init=False)

        def set_optional_data(self, training):
            self.training = training

    def _process_words(self, words: list[str]) -> None:
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

        self.attrs = self.Attrs(start_dt.timestamp(), end_dt.timestamp(), gym)
        try:
            training = words[2]
        except IndexError:
            training = None

        self.attrs.set_optional_data(training)

    def _upload_keiko(self, unit_key):
        gym = Gym(start_t=self.attrs.start_t,
                  end_t=self.attrs.end_t,
                  gym=self.attrs.gym,
                  training=self.attrs.training,
                  unit=unit_key)
        with Session(self.engine) as session:
            session.add(gym)
            session.commit()

