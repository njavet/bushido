import datetime
from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped, Session

# project imports
from bushido.data.categories.category import (AbsReceiver,
                                              AbsUploader,
                                              AbsKeikoTable)


class Receiver(AbsReceiver):
    def __init__(self, engine):
        super().__init__(engine)
        self.keiko = KeikoTable


class Uploader(AbsUploader):
    def __init__(self, engine):
        super().__init__(engine)

    def upload_unit(self, unit_spec, keiko_spec):
        unit = self.create_orm_unit(unit_spec)
        keiko = self.create_orm_unit(keiko_spec)
        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            keiko.fk_unit = unit.key
            session.add(keiko)
            session.commit()

    def create_orm_keiko(self, keiko_spce):
        keiko = KeikoTable(start_t=keiko_spce.start_t,
                           end_t=keiko_spce.end_t,
                           gym=keiko_spce.gym)
        return keiko


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'gym'

    start_t: Mapped[int] = mapped_column(BigInteger)
    end_t: Mapped[int] = mapped_column(BigInteger)
    gym: Mapped[str] = mapped_column()
