from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from ulib.abs_category import AbsCategory, AbsProcessor, AbsKeikoTable


class Category(AbsCategory):
    def __init__(self, name, engine):
        super().__init__(name, engine)


class Processor(AbsProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    def process_keiko(self, unit, words):
        try:
            weights = [float(w) for w in words[::3]]
            reps = [float(r) for r in words[1::3]]
            pauses = [int(p) for p in words[2::3]] + [0]
        except ValueError:
            raise ValueError('invalid input')

        if len(reps) != len(weights):
            raise ValueError(
                'Not the same number of reps and weights')
        if len(pauses) != len(reps):
            raise ValueError('break error')
        if len(reps) < 1:
            raise ValueError('No set')

        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            keikos = []
            for set_nr, (w, r, p) in enumerate(zip(weights, reps, pauses)):
                keiko = KeikoTable(set_nr=set_nr,
                                   weight=w,
                                   reps=r,
                                   pause=p,
                                   fk_unit=unit.key)
                keikos.append(keiko)
            session.add_all(keikos)
            session.commit()


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)
