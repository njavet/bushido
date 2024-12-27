from dataclasses import dataclass, field
import datetime

# project imports
from .unit_processor_factory import UnitProcessorFactory
from ulib.parsing import parse_start_end_time_string


class UnitProcessor(UnitProcessorFactory):
    def __init__(self):
        super().__init__()

    @dataclass
    class Attrs:
        start_t: float
        end_t: float
        gym: str
        training: str | None = field(init=False)

        def set_optional_data(self, training):
            self.training = training

    def process_words(self, words: list[str]) -> None:
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
