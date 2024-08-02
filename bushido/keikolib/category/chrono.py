from dataclasses import dataclass
import peewee as pw

# project imports
from bushido.keikolib.abscat import Keiko, AbsProcessor, AbsRetriever, AbsUmojis
from bushido.keikolib.parsing import parse_time_string


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


class Retriever(AbsRetriever):
    def __init__(self, category: str, uname: str) -> None:
        super().__init__(category, uname)
        self.keiko = Chrono


class Chrono(Keiko):
    seconds = pw.FloatField()


class Umojis(AbsUmojis):

    umoji2uname = {
           b'\xe2\x9a\x94\xef\xb8\x8f'.decode(): 'splitmachine',
           b'\xf0\x9f\x8f\xb9'.decode(): 'stretch',
           b'\xf0\x9f\x94\xa5'.decode(): 'naulikriya'}
    emoji2umoji = {
           # sword -> split_machine
           b'\xe2\x9a\x94'.decode(): b'\xe2\x9a\x94\xef\xb8\x8f'.decode()}

