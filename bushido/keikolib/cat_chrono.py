from dataclasses import dataclass
import peewee as pw

# project imports
from bushido.keikolib.abscat import Keiko, AbsProcessor, AbsCategory, AbsUmojis
from bushido.keikolib.parsing import parse_time_string


class Category(AbsCategory):
    def __init__(self, category: str) -> None:
        super().__init__(category)
        self.keiko = Chrono


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    @dataclass
    class Attrs:
        seconds: float

    def _process_words(self, words):
        seconds = parse_time_string(words[0])
        self.attrs = self.Attrs(seconds=seconds)

    def _save_keiko(self, unit):
        Chrono.create(unit_id=unit, seconds=self.attrs.seconds)

