from sqlalchemy.orm import mapped_column, Mapped, Session

# project imports
from ulib.abs_category import AbsCategory, AbsProcessor, AbsKeikoTable


class Category(AbsCategory):
    def __init__(self, name, engine):
        super().__init__(name, engine)


class Processor(AbsProcessor):
    def __init__(self, engine):
        super().__init__(engine)

    def process_keiko(self, unit, words):
        start_t, end_t = parse_start_end_time_string(words[0])
        try:
            gym = words[1]
        except IndexError:
            raise ValueError('no gym')

        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            keiko = KeikoTable(start_t=start_t,
                               end_t=end_t,
                               gym=gym,
                               fk_unit=unit.key)
            session.add(keiko)
            session.commit()


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'gym'

    start_t: Mapped[float] = mapped_column()
    end_t: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()



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
