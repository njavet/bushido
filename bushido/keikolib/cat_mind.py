from dataclasses import dataclass, field
import peewee as pw

# project imports
from bushido.keikolib.abscat import Keiko, AbsProcessor, AbsCategory, AbsUmojis
from bushido.keikolib.parsing import parse_time_string


class Category(AbsCategory):
    def __init__(self, category: str) -> None:
        super().__init__(category)
        self.keiko = Mind


class Processor(AbsProcessor):
    def __init__(self, category, uname, umoji):
        super().__init__(category, uname, umoji)

    @dataclass
    class Attrs:
        seconds: float
        topic: str
        focus: str | None = field(init=False)

        def set_optional_data(self, focus):
            self.focus = focus

    def _process_words(self, words):
        seconds = parse_time_string(words[0])
        try:
            topic = words[1]
        except IndexError:
            raise ValueError('no topic')

        try:
            focus = words[2]
        except IndexError:
            focus = None

        self.attrs = self.Attrs(seconds=seconds,
                                topic=topic)
        self.attrs.set_optional_data(focus)

    def _save_keiko(self, unit):
        Mind.create(unit_id=unit,
                    seconds=self.attrs.seconds,
                    topic=self.attrs.topic,
                    focus=self.attrs.focus)


class Mind(Keiko):
    seconds = pw.FloatField()
    topic = pw.CharField()
    focus = pw.CharField(null=True)
    # unix utc timestamps
    start_t = pw.FloatField(null=True)
    end_t = pw.FloatField(null=True)
    breaks = pw.IntegerField(null=True)


class Umojis(AbsUmojis):
    umoji2uname = {
           b'\xf0\x9f\x93\xa1'.decode(): 'study',
           b'\xf0\x9f\x9b\xb0\xef\xb8\x8f'.decode(): 'exam',
           b'\xf0\x9f\xa6\x89'.decode(): 'reading'}
    emoji2umoji = {
           # orbital -> exam
           b'\xf0\x9f\x9b\xb0'.decode(): b'\xf0\x9f\x9b\xb0\xef\xb8\x8f'.decode()}

