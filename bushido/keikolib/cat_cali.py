import peewee as pw
from dataclasses import dataclass

# project imports
from bushido.keikolib.abscat import Keiko, AbsProcessor, AbsCategory, AbsUmojis


class Category(AbsCategory):
    def __init__(self, category: str) -> None:
        super().__init__(category)
        self.keiko = Cali


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    @dataclass
    class Attrs:
        sets: list[int]
        reps: list[float]
        pauses: list[int]

        def zipped(self):
            return zip(self.sets, self.reps, self.pauses)

    def _process_words(self, words) -> None:
        try:
            reps = [float(w) for w in words[::2]]
            pauses = [int(p) for p in words[1::2]] + [0]
        except ValueError:
            raise ValueError('invalid input')

        if len(pauses) != len(reps):
            raise ValueError('break error')
        if len(reps) < 1:
            raise ValueError('No set')

        self.attrs = self.Attrs(sets=list(range(len(reps))),
                                reps=reps,
                                pauses=pauses)

    def _save_keiko(self, unit):
        for set_nr, r, p in self.attrs.zipped():
            Cali.create(unit_id=unit,
                        set_nr=set_nr,
                        reps=r,
                        pause=p)

