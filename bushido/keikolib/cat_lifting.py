import peewee as pw
from dataclasses import dataclass

# project imports
from bushido.keikolib.abscat import Keiko, AbsProcessor, AbsCategory, AbsUmojis


class Category(AbsCategory):
    def __init__(self, category: str) -> None:
        super().__init__(category)
        self.keiko = Lifting


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

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

    def _save_keiko(self, unit):
        for set_nr, w, r, p in self.attrs.zipped():
            Lifting.create(unit_id=unit,
                           set_nr=set_nr,
                           weight=w,
                           reps=r,
                           pause=p)
