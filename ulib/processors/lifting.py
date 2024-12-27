from dataclasses import dataclass

# project imports
from .unit_processor_factory import UnitProcessorFactory


class UnitProcessor(UnitProcessorFactory):
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

    def process_words(self, words) -> None:
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
