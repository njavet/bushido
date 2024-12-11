from dataclasses import dataclass
from sqlalchemy.orm import Session

# project imports
from ulib.db.models import Wimhof
from ulib.processors import AbsUnitProcessor


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    @dataclass
    class Attrs:
        rounds: list[int]
        breaths: list[int]
        retentions: list[int]

        def zipped(self):
            return zip(self.rounds, self.breaths, self.retentions)

    def _process_words(self, words):
        try:
            breaths = [int(b) for b in words[::2]]
            retentions = [int(r) for r in words[1::2]]
        except ValueError:
            raise ValueError('value error')
        if len(breaths) != len(retentions):
            raise ValueError('Not the same number of breaths and seconds')
        if len(breaths) < 1:
            raise ValueError('At least one round necessary')

        self.attrs = self.Attrs(rounds=list(range(len(breaths))),
                                breaths=breaths,
                                retentions=retentions)

    def _upload_keiko(self, unit_key):
        upload_lst = []
        for round_nr, b, r in self.attrs.zipped():
            wimhof = Wimhof(round_nr=round_nr,
                            breaths=b,
                            retention=r,
                            unit=unit_key)
            upload_lst.append(wimhof)
        with Session(self.engine) as session:
            session.add_all(upload_lst)
            session.commit()

