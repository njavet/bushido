from dataclasses import dataclass, field
import peewee as pw

# project imports
import unit_processing
import exceptions
import parsing


class UnitProcessor(unit_processing.UnitProcessor):
    def __init__(self, module_name, unit_name, unit_emoji):
        super().__init__(module_name, unit_name, unit_emoji)

    def parse_words(self, words):
        seconds = parsing.parse_time_string(words[0])
        try:
            topic = words[1]
        except IndexError:
            raise exceptions.UnitProcessingError('no topic')

        try:
            focus = words[2]
        except IndexError:
            focus = None

        self.attrs = Attrs(seconds=seconds,
                           topic=topic)
        self.attrs.set_optional_data(focus)

    def save_subunit(self):
        self.subunit = Mind.create(unit_id=self.unit,
                                   seconds=self.attrs.seconds,
                                   topic=self.attrs.topic,
                                   focus=self.attrs.focus)


@dataclass
class Attrs(unit_processing.Attrs):
    seconds: float
    topic: str
    focus: str | None = field(init=False)

    def set_optional_data(self, focus):
        self.focus = focus


class Mind(unit_processing.SubUnit):
    seconds = pw.FloatField()
    topic = pw.CharField()
    focus = pw.CharField(null=True)
