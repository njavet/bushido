from dataclasses import dataclass, field
from sqlalchemy.orm import Session
import datetime

# project imports
from bushido.db.models import Gym
from bushido.services.units.abs_unit_proc import AbsUnitProcessor
from bushido.parsing import parse_start_end_time_string


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine, emoji2key):
        super().__init__(engine, emoji2key)

    @dataclass
    class Attrs:
        start_t: datetime.time
        end_t: datetime.time
        gym: str
        training: str | None = field(init=False)

        def set_optional_data(self, training):
            self.training = training

    def _process_words(self, words: list[str]) -> None:
        start_t, end_t = parse_start_end_time_string(words[0])
        try:
            gym = words[1]
        except IndexError:
            raise ValueError('no gym')

        self.attrs = self.Attrs(start_t, end_t, gym)
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

