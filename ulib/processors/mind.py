from dataclasses import dataclass, field
from sqlalchemy.orm import Session

# project imports
from ulib.db.models import Mind
from ulib.processors import AbsUnitProcessor
from ulib.parsing.parsing import parse_time_string


class UnitProcessor(AbsUnitProcessor):
    def __init__(self, engine):
        super().__init__(engine)

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

    def _upload_keiko(self, unit_key):
        mind = Mind(seconds=self.attrs.seconds,
                    topic=self.attrs.topic,
                    focus=self.attrs.focus,
                    unit=unit_key)
        with Session(self.engine) as session:
            session.add(mind)
            session.commit()

