from sqlalchemy.orm import Mapped, mapped_column

# project imports
from ulib.db.tables.base import KeikoTable


class LiftingTable(KeikoTable):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)
from sqlalchemy.orm import Session

# project imports
from ulib.db.uploaders.base import BaseUploader
from ulib.db.tables.lifting import LiftingTable


class LiftingUploader(BaseUploader):
    def __init__(self, engine):
        super().__init__(engine)

    def _upload_unit(self, attrs):
        with Session(self.engine) as session:
            session.add(self.unit)
            session.commit()
            keikos = []
            for set_nr, w, r, p in attrs.zipped():
                lifting = LiftingTable(set_nr=set_nr,
                                       weight=w,
                                       reps=r,
                                       pause=p,
                                       fk_unit=self.unit.key)
                keikos.append(lifting)
            session.add_all(keikos)
            session.commit()
from dataclasses import dataclass

# project imports
from ulib.parsers.base_parser import BaseParser


class LiftingParser(BaseParser):
    def __init__(self):
        super().__init__()

    @dataclass
    class Attrs:
        sets: list[int]
        weights: list[float]
        reps: list[float]
        pauses: list[int]

        def zipped(self):
            return zip(self.sets, self.weights, self.reps, self.pauses)

    def parse_words(self, words) -> Attrs:
        try:
            weights = [float(w) for w in words[::3]]
            reps = [float(r) for r in words[1::3]]
            pauses = [int(p) for p in words[2::3]] + [0]
        except ValueError:
            raise ValueError('invalid input')

        if len(reps) != len(weights):
            raise ValueError(
                'Not the same number of reps and weights')
        if len(pauses) != len(reps):
            raise ValueError('break error')
        if len(reps) < 1:
            raise ValueError('No set')

        attrs = self.Attrs(sets=list(range(len(weights))),
                           weights=weights,
                           reps=reps,
                           pauses=pauses)
        return attrs
