# general imports
import peewee as pw

# project imports
import db
import umodule
from utils import exceptions


class UnitProcessor(umodule.UnitProcessor):
    def __init__(self, module_name, unit_name, emoji):
        super().__init__(module_name, unit_name, emoji)

    def subunit_handler(self, words):
        attributes = self.parse_words(words)
        for set_nr, attrs in attributes.items():
            Lifting.create(
                unit_id=self.unit.id,
                set_nr=set_nr,
                weight=attrs["weight"],
                reps=attrs["reps"],
                pause=attrs["pause"],
            )

    @classmethod
    def parse_words(cls, words):
        try:
            weights = [float(w) for w in words[::3]]
            reps = [float(r) for r in words[1::3]]
            pauses = [float(p) for p in words[2::3]] + [0]
        except ValueError:
            raise exceptions.UnitProcessingError("invalid input")

        if len(reps) != len(weights):
            raise exceptions.UnitProcessingError(
                "Not the same number of reps and weights"
            )
        if len(pauses) != len(reps):
            raise exceptions.UnitProcessingError("break error")
        if len(reps) < 1:
            raise exceptions.UnitProcessingError("No set")

        attributes = {}
        for i, (weight, reps, pause) in enumerate(zip(weights, reps, pauses)):
            attributes[i] = {"weight": weight, "reps": reps, "pause": pause}
        return attributes


class Lifting(db.SubUnit):
    set_nr = pw.IntegerField()
    weight = pw.FloatField()
    reps = pw.FloatField()
    pause = pw.IntegerField()

    def __str__(self):
        return " ".join([str(self.weight), str(self.reps), str(self.pause)])
