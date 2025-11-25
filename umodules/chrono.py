# general imports
import peewee as pw

# project imports
import umodule
import parsing
import db


class UnitProcessor(umodule.UnitProcessor):
    def __init__(self, module_name, unit_name, emoji):
        super().__init__(module_name, unit_name, emoji)

    def subunit_handler(self, words):
        self.subunit = Chrono(**self.parse_words(words))
        self.subunit.unit_id = self.unit.id
        self.subunit.save()

    @classmethod
    def parse_words(cls, words):
        seconds = parsing.parse_time_string(words[0])
        return {'seconds': seconds}


class Chrono(db.SubUnit):
    seconds = pw.FloatField()

