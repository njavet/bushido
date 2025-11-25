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
        for round_nr, attrs in attributes.items():
            Wimhof.create(unit_id=self.unit.id, round_nr=round_nr, **attrs)

    @classmethod
    def parse_words(cls, words):
        try:
            breaths = [int(b) for b in words[::2]]
            retentions = [int(r) for r in words[1::2]]
        except ValueError:
            raise exceptions.UnitProcessingError("value error")
        if len(breaths) != len(retentions):
            raise exceptions.UnitProcessingError(
                "Not the same number of breaths and seconds"
            )
        if len(breaths) < 1:
            raise exceptions.UnitProcessingError("At least one round necessary")

        attributes = {}
        for round_nr, (b, r) in enumerate(zip(breaths, retentions)):
            attributes[round_nr] = {"breaths": b, "retention": r}
        return attributes


class Wimhof(db.SubUnit):
    round_nr = pw.IntegerField()
    breaths = pw.IntegerField()
    retention = pw.IntegerField()
