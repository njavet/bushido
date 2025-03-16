import datetime
from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped, Session

# project imports
from bushido.data._category import AbsCategory, AbsProcessor, AbsKeikoTable
from bushido.utils.parsing import parse_start_end_time_string


class Category(AbsCategory):
    def __init__(self, engine):
        super().__init__(engine)
        self.keiko = KeikoTable


class Processor(AbsProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    def process_keiko(self, unit, words):
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

        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            keiko = KeikoTable(start_t=int(start_dt.timestamp()),
                               end_t=int(end_dt.timestamp()),
                               gym=gym,
                               fk_unit=unit.key)
            session.add(keiko)
            session.commit()


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'gym'

    start_t: Mapped[int] = mapped_column(BigInteger)
    end_t: Mapped[int] = mapped_column(BigInteger)
    gym: Mapped[str] = mapped_column()
