import peewee as pw
from dataclasses import dataclass

# project imports
from bushido.keiko import Keiko, AbsProcessor, AbsRetriever, AbsAttrs, AbsUmojis
from bushido.exceptions import ProcessingError


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    def _process_words(self, words) -> None:
        try:
            reps = [float(w) for w in words[::2]]
            pauses = [int(p) for p in words[1::2]] + [0]
        except ValueError:
            raise ProcessingError('invalid input')

        if len(pauses) != len(reps):
            raise ProcessingError('break error')
        if len(reps) < 1:
            raise ProcessingError('No set')

        self.attrs = Attrs(sets=list(range(len(reps))),
                           reps=reps,
                           pauses=pauses)

    def _save_keiko(self, unit):
        for set_nr, r, p in self.attrs.zipped():
            Cali.create(unit_id=unit,
                        set_nr=set_nr,
                        reps=r,
                        pause=p)


@dataclass
class Attrs(AbsAttrs):
    sets: list[int]
    reps: list[float]
    pauses: list[int]

    def zipped(self):
        return zip(self.sets, self.reps, self.pauses)


class Cali(Keiko):
    set_nr = pw.IntegerField()
    reps = pw.FloatField()
    pause = pw.IntegerField()


class Umojis(AbsUmojis):
    umoji2uname = {b'\xf0\x9f\xa6\x85'.decode(): 'pullups'}
