from dataclasses import dataclass, field
import datetime
import peewee as pw

# project imports
import exceptions
import unit_processing
import parsing


class UnitProcessor(unit_processing.UnitProcessor):
    def __init__(self, module_name, unit_name, unit_emoji):
        super().__init__(module_name, unit_name, unit_emoji)

    def parse_words(self, words):
        start_t, end_t = parsing.parse_start_end_time_string(words[0])
        try:
            gym = words[1]
        except IndexError:
            raise exceptions.UnitProcessingError('no gym')

        self.attrs = Attrs(start_t, end_t, gym)
        try:
            training = words[2]
        except IndexError:
            training = None

        self.attrs.set_optional_data(training)

    def save_subunit(self):
        self.subunit = Gym.create(unit_id=self.unit,
                                  start_t=self.attrs.start_t,
                                  end_t=self.attrs.end_t,
                                  gym=self.attrs.gym,
                                  training=self.attrs.training)


@dataclass
class Attrs(unit_processing.Attrs):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = field(init=False)

    def set_optional_data(self, training):
        self.training = training


class Gym(unit_processing.SubUnit):
    start_t = pw.TimeField()
    end_t = pw.TimeField()
    gym = pw.CharField()
    training = pw.CharField(null=True)

