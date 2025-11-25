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
        self.subunit = Gym(**self.parse_words(words))
        self.subunit.unit_id = self.unit.id
        self.subunit.save()

    @classmethod
    def parse_words(cls, words):
        start_t, end_t = parsing.parse_start_end_time_string(words[0])
        attributes = {'start_t': start_t, 'end_t': end_t, 'gym': words[1]}
        try:
            attributes['training'] = words[2]
        except IndexError:
            pass
        return attributes


class Gym(db.SubUnit):
    start_t = pw.TimeField()
    end_t = pw.TimeField()
    gym = pw.CharField()
    training = pw.CharField(null=True)

