from dataclasses import dataclass
import peewee as pw

# project imports
import unit_processing
import parsing


class UnitProcessor(unit_processing.UnitProcessor):
    def __init__(self, module_name, unit_name, unit_emoji):
        super().__init__(module_name, unit_name, unit_emoji)

    def parse_words(self, words):
        seconds = parsing.parse_time_string(words[0])
        self.attrs = Attrs(seconds=seconds)

    def save_subunit(self):
        self.subunit = Chrono.create(unit_id=self.unit,
                                     seconds=self.attrs.seconds)


@dataclass
class Attrs(unit_processing.Attrs):
    seconds: float


class Chrono(unit_processing.SubUnit):
    seconds = pw.FloatField()
