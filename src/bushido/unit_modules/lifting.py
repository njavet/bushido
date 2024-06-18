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
            weights = [float(w) for w in words[::3]]
            reps = [float(r) for r in words[1::3]]
            pauses = [int(p) for p in words[2::3]] + [0]
        except ValueError:
            raise exceptions.UnitProcessingError('invalid input')

        if len(reps) != len(weights):
            raise exceptions.UnitProcessingError(
                'Not the same number of reps and weights')
        if len(pauses) != len(reps):
            raise exceptions.UnitProcessingError('break error')
        if len(reps) < 1:
            raise exceptions.UnitProcessingError('No set')

        self.attrs = Attrs(sets=list(range(len(weights))),
                           weights=weights,
                           reps=reps,
                           pauses=pauses)

    def save_subunit(self):
        for set_nr, w, r, p in self.attrs.zipped():
            Lifting.create(unit_id=self.unit,
                           set_nr=set_nr,
                           weight=w,
                           reps=r,
                           pause=p)


@dataclass
class Attrs(unit_processing.Attrs):
    sets: list[int]
    weights: list[float]
    reps: list[float]
    pauses: list[int]

    def zipped(self):
        return zip(self.sets, self.weights, self.reps, self.pauses)


class Lifting(unit_processing.SubUnit):
    set_nr = pw.IntegerField()
    weight = pw.FloatField()
    reps = pw.FloatField()
    pause = pw.IntegerField()

    def __str__(self):
        return ' '.join([str(self.weight), str(self.reps), str(self.pause)])

