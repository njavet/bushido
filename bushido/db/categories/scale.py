from sqlalchemy.orm import mapped_column, Mapped, Session

# project imports
from bushido.db.base_category import AbsCategory, AbsProcessor, AbsKeikoTable


class Category(AbsCategory):
    def __init__(self, name, engine):
        super().__init__(name, engine)


class Processor(AbsProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    def process_keiko(self, unit, words):
        try:
            weight = float(words[0])
        except (IndexError, ValueError):
            raise ValueError('wrong format')

        try:
            fat = float(words[1])
        except IndexError:
            fat = None

        try:
            water = float(words[2])
        except IndexError:
            water = None

        try:
            muscles = float(words[3])
        except IndexError:
            muscles = None

        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            keiko = KeikoTable(weight=weight,
                               fat=fat,
                               water=water,
                               muscles=muscles,
                               fk_unit=unit.key)
            session.add(keiko)
            session.commit()


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'scale'

    weight: Mapped[float] = mapped_column()
    fat: Mapped[float] = mapped_column()
    water: Mapped[float] = mapped_column()
    muscles: Mapped[float] = mapped_column()
