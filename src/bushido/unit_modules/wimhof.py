from dataclasses import dataclass
import peewee as pw

# project imports
import unit_processing
import exceptions


class UnitProcessor(unit_processing.UnitProcessor):
    def __init__(self, module_name, unit_name, unit_emoji):
        super().__init__(module_name, unit_name, unit_emoji)

    def parse_words(self, words):
        try:
            breaths = [int(b) for b in words[::2]]
            retentions = [int(r) for r in words[1::2]]
        except ValueError:
            raise exceptions.UnitProcessingError('value error')
        if len(breaths) != len(retentions):
            raise exceptions.UnitProcessingError('Not the same number of breaths and seconds')
        if len(breaths) < 1:
            raise exceptions.UnitProcessingError('At least one round necessary')

        self.attrs = Attrs(rounds=list(range(len(breaths))),
                           breaths=breaths,
                           retentions=retentions)

    def save_subunit(self):
        for round_nr, b, r in self.attrs.zipped():
            Wimhof.create(unit_id=self.unit,
                          round_nr=round_nr,
                          breaths=b,
                          retention=r)


@dataclass
class Attrs(unit_processing.Attrs):
    rounds: list[int]
    breaths: list[int]
    retentions: list[int]

    def zipped(self):
        return zip(self.rounds, self.breaths, self.retentions)


class Wimhof(unit_processing.SubUnit):
    round_nr = pw.IntegerField()
    breaths = pw.IntegerField()
    retention = pw.IntegerField()
