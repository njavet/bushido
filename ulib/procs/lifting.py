from dataclasses import dataclass
from sqlalchemy.orm import Session

# project imports
from bushido.db.models import Lifting
from bushido.procs.abs_unit_proc import AbsUnitProcessor


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    @dataclass
    class Attrs:
        sets: list[int]
        weights: list[float]
        reps: list[float]
        pauses: list[int]

        def zipped(self):
            return zip(self.sets, self.weights, self.reps, self.pauses)

    def _process_words(self, words) -> None:
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

        self.attrs = self.Attrs(sets=list(range(len(weights))),
                                weights=weights,
                                reps=reps,
                                pauses=pauses)

    def _upload_keiko(self, unit_key):
        upload_lst = []
        for set_nr, w, r, p in self.attrs.zipped():
            lifting = Lifting(set_nr=set_nr,
                              weight=w,
                              reps=r,
                              pause=p,
                              unit=unit_key)
            upload_lst.append(lifting)
        with Session(self.engine) as session:
            session.add_all(upload_lst)
            session.commit()
