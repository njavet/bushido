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
            weights = [float(w) for w in words[::3]]
            reps = [float(r) for r in words[1::3]]
            pauses = [int(p) for p in words[2::3]] + [0]
        except ValueError:
            raise ProcessingError('invalid input')

        if len(reps) != len(weights):
            raise ProcessingError(
                'Not the same number of reps and weights')
        if len(pauses) != len(reps):
            raise ProcessingError('break error')
        if len(reps) < 1:
            raise ProcessingError('No set')

        self.attrs = Attrs(sets=list(range(len(weights))),
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


@dataclass
class Attrs(AbsAttrs):
    sets: list[int]
    weights: list[float]
    reps: list[float]
    pauses: list[int]

    def zipped(self):
        return zip(self.sets, self.weights, self.reps, self.pauses)


class Lifting(Keiko):
    set_nr = pw.IntegerField()
    weight = pw.FloatField()
    reps = pw.FloatField()
    pause = pw.IntegerField()

    def __str__(self):
        return ' '.join([str(self.weight), str(self.reps), str(self.pause)])


class Umojis(AbsUmojis):
    umoji2uname = {
            b'\xe2\x9b\xa9\xef\xb8\x8f'.decode(): 'squat',
            b'\xf0\x9f\x8f\x97\xef\xb8\x8f'.decode(): 'deadlift',
            b'\xf0\x9f\x9a\x81'.decode(): 'benchpress',
            b'\xf0\x9f\xa6\xad'.decode(): 'overheadpress',
            b'\xf0\x9f\x90\xa2'.decode(): 'rows'}
    emoji2umoji = {
            # shinto -> squats
            b'\xe2\x9b\xa9'.decode(): b'\xe2\x9b\xa9\xef\xb8\x8f'.decode(),
            # crane -> deadlift'
            b'\xf0\x9f\x8f\x97'.decode(): b'\xf0\x9f\x8f\x97\xef\xb8\x8f'.decode()}

