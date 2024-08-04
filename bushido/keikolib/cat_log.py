from dataclasses import dataclass
import peewee as pw

# project imports
from bushido.keikolib.abscat import Keiko, AbsProcessor, AbsCategory, AbsUmojis


class Category(AbsCategory):
    def __init__(self, category: str) -> None:
        super().__init__(category)
        self.keiko = Log


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    @dataclass
    class Attrs:
        log_str: str

    def _process_words(self, words: list) -> None:
        try:
            log_str = words[0]
        except IndexError:
            raise ValueError('empty log')

        self.attrs = self.Attrs(log_str=log_str)

    def _save_keiko(self, unit):
        Log.create(unit_id=unit,
                   log_str=self.attrs.log_str)


class Log(Keiko):
    log_str = pw.CharField()


class Umojis(AbsUmojis):
    umoji2uname = {b'\xf0\x9f\x8c\x90'.decode(): 'log'}

