import datetime
from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped, Session

# project imports
from bushido.data.category import AbsCategory, AbsKeikoTable


class Category(AbsCategory):
    def __init__(self, engine):
        super().__init__(engine)
        self.keiko = KeikoTable


class Processor(AbsProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    def process_keiko(self, unit, words):
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
