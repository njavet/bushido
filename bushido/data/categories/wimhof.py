from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from bushido.data.categories import AbsCategory, AbsProcessor, AbsKeikoTable


class Category(AbsCategory):
    def __init__(self, engine):
        super().__init__(engine)
        self.keiko = KeikoTable


class Processor(AbsProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    def process_keiko(self, unit, words):
        try:
            breaths = [float(bs) for bs in words[::2]]
            retentions = [float(r) for r in words[1::2]]
        except ValueError:
            raise ValueError('invalid input')

        if len(breaths) != len(retentions):
            raise ValueError(
                'Not the same number of breaths and retentions')
        if len(retentions) < 1:
            raise ValueError('No round')

        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            keikos = []
            for round_nr, (b, r) in enumerate(zip(breaths, retentions)):
                keiko = KeikoTable(round_nr=round_nr,
                                   breaths=b,
                                   retention=r,
                                   fk_unit=unit.key)
                keikos.append(keiko)
            session.add_all(keikos)
            session.commit()


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'wimhof'

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()
