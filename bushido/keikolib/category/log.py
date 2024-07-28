from dataclasses import dataclass
import peewee as pw

# project imports
from bushido.keiko import Keiko, AbsProcessor, AbsRetriever, AbsAttrs, AbsUmojis
from bushido.exceptions import ProcessingError


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    def _process_words(self, words: list) -> None:
        try:
            log_str = words[0]
        except IndexError:
            raise ProcessingError('empty log')

        self.attrs = Attrs(log_str=log_str)

    def _save_keiko(self, unit):
        Log.create(unit_id=unit,
                   log_str=self.attrs.log_str)


@dataclass
class Attrs(AbsAttrs):
    log_str: str


class Log(Keiko):
    log_str = pw.CharField()


class Umojis(AbsUmojis):
    umoji2uname = {b'\xf0\x9f\x8c\x90'.decode(): 'log'}

