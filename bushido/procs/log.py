from dataclasses import dataclass
from sqlalchemy.orm import Session

# project imports
from bushido.db.models import Log
from bushido.services.units.abs_unit_proc import AbsUnitProcessor


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine, emoji2key):
        super().__init__(engine, emoji2key)

    @dataclass
    class Attrs:
        log_str: str

    def _process_words(self, words: list) -> None:
        try:
            log_str = words[0]
        except IndexError:
            raise ValueError('empty log')

        self.attrs = self.Attrs(log_str=log_str)

    def _upload_keiko(self, unit_key):
        log = Log(log=self.attrs.log_str,
                  unit=unit_key)
        with Session(self.engine) as session:
            session.add(log)
            session.commit()
