from dataclasses import dataclass, field
import datetime
import peewee as pw

# project imports
from bushido.keiko import Keiko, AbsProcessor, AbsRetriever, AbsAttrs, AbsUmojis
from bushido.parsing import parse_start_end_time_string
from bushido.exceptions import ProcessingError


class Gym(Keiko):
    start_t = pw.TimeField()
    end_t = pw.TimeField()
    gym = pw.CharField()
    training = pw.CharField(null=True)


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    def _process_words(self, words: list[str]) -> None:
        start_t, end_t = parse_start_end_time_string(words[0])
        try:
            gym = words[1]
        except IndexError:
            raise ProcessingError('no gym')

        self.attrs = Attrs(start_t, end_t, gym)
        try:
            training = words[2]
        except IndexError:
            training = None

        self.attrs.set_optional_data(training)

    def _save_keiko(self, unit):
        Gym.create(unit_id=unit,
                   start_t=self.attrs.start_t,
                   end_t=self.attrs.end_t,
                   gym=self.attrs.gym,
                   training=self.attrs.training)


class Retriever(AbsRetriever):
    pass


@dataclass
class Attrs(AbsAttrs):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = field(init=False)

    def set_optional_data(self, training):
        self.training = training


class Umojis(AbsUmojis):
    umoji2uname = {b'\xf0\x9f\xa6\x8d'.decode(): 'weights',
                   b'\xf0\x9f\xa5\x8b'.decode(): 'martial_arts',
                   b'\xe2\x9a\x93\xef\xb8\x8f'.decode(): 'yoga'}
    # anchor emoji for yoga
    emoji2umoji = {b'\xe2\x9a\x93'.decode(): b'\xe2\x9a\x93\xef\xb8\x8f'.decode()}
