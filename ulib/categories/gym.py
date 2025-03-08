from sqlalchemy.orm import mapped_column, Mapped

# project imports
from ulib.db.tables.base import KeikoTable


class GymTable(KeikoTable):
    __tablename__ = 'gym'

    start_t: Mapped[float] = mapped_column()
    end_t: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()
from sqlalchemy.orm import Session

# project imports
from ulib.db.tables.gym import GymTable
from ulib.db.uploaders.base import BaseUploader


class GymUploader(BaseUploader):
    def __init__(self, engine):
        super().__init__(engine)

    def _upload_unit(self, attrs):
        with Session(self.engine) as session:
            session.add(self.unit)
            session.commit()
            keiko = GymTable(start_t=attrs.start_t,
                             end_t=attrs.end_t,
                             gym=attrs.gym,
                             fk_unit=self.unit.key)
            session.add(keiko)
            session.commit()
from dataclasses import dataclass, field
import datetime

# project imports
from ulib.parsers.base_parser import BaseParser
from ulib.utils.parsing import parse_start_end_time_string


class GymParser(BaseParser):
    def __init__(self):
        super().__init__()

    @dataclass
    class Attrs:
        start_t: float
        end_t: float
        gym: str
        training: str | None = field(init=False)

        def set_optional_data(self, training):
            self.training = training

    def parse_words(self, words: list[str]) -> Attrs:
        today = datetime.date.today()
        start_t, end_t = parse_start_end_time_string(words[0])
        start_dt = datetime.datetime(today.year,
                                     today.month,
                                     today.day,
                                     start_t.hour,
                                     start_t.minute)
        end_dt = datetime.datetime(today.year,
                                   today.month,
                                   today.day,
                                   end_t.hour,
                                   end_t.minute)
        try:
            gym = words[1]
        except IndexError:
            raise ValueError('no gym')

        attrs = self.Attrs(start_dt.timestamp(), end_dt.timestamp(), gym)
        try:
            training = words[2]
        except IndexError:
            training = None

        attrs.set_optional_data(training)
        return attrs
