import peewee as pw
from dataclasses import dataclass

# project imports
import unit_processing
import exceptions


class UnitProcessor(unit_processing.UnitProcessor):
    def __init__(self, module_name, unit_name, unit_emoji):
        super().__init__(module_name, unit_name, unit_emoji)

    def parse_words(self, words) -> None:
        try:
            reps = [float(w) for w in words[::2]]
            pauses = [int(p) for p in words[1::2]] + [0]
        except ValueError:
            raise exceptions.UnitProcessingError('invalid input')

        if len(pauses) != len(reps):
            raise exceptions.UnitProcessingError('break error')
        if len(reps) < 1:
            raise exceptions.UnitProcessingError('No set')

        self.attrs = Attrs(sets=list(range(len(reps))),
                           reps=reps,
                           pauses=pauses)

    def save_subunit(self):
        for set_nr, r, p in self.attrs.zipped():
            Cali.create(unit_id=self.unit,
                        set_nr=set_nr,
                        reps=r,
                        pause=p)


@dataclass
class Attrs(unit_processing.Attrs):
    sets: list[int]
    reps: list[float]
    pauses: list[int]

    def zipped(self):
        return zip(self.sets, self.reps, self.pauses)


class Cali(unit_processing.SubUnit):
    set_nr = pw.IntegerField()
    reps = pw.FloatField()
    pause = pw.IntegerField()
