from dataclasses import dataclass
from sqlalchemy.orm import Session

# project imports
from ulib.processors import AbsUnitProcessor
from ulib.db.models import Chrono
from ulib.parsing.parsing import parse_time_string


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    @dataclass
    class Attrs:
        seconds: float

    def _process_words(self, words):
        seconds = parse_time_string(words[0])
        self.attrs = self.Attrs(seconds=seconds)

    def _upload_keiko(self, unit_key):
        chrono = Chrono(seconds=self.attrs.seconds,
                        unit=unit_key)
        with Session(self.engine) as session:
            session.add(chrono)
            session.commit()

