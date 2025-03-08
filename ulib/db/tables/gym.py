from sqlalchemy.orm import mapped_column, Mapped, Session

# project imports
from ulib.db.tables.base import KeikoTable, BaseUploader


class GymTable(KeikoTable):
    __tablename__ = 'gym'

    start_t: Mapped[float] = mapped_column()
    end_t: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()


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
