from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from ulib.db.tables.base import KeikoTable, BaseUploader


class LiftingTable(KeikoTable):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)


class LiftingUploader(BaseUploader):
    def __init__(self, engine):
        super().__init__(engine)

    def _upload_unit(self, attrs):
        with Session(self.engine) as session:
            session.add(self.unit)
            session.commit()
            keikos = []
            for set_nr, w, r, p in attrs.zipped():
                lifting = LiftingTable(set_nr=set_nr,
                                       weight=w,
                                       reps=r,
                                       pause=p,
                                       fk_unit=self.unit.key)
                keikos.append(lifting)
            session.add_all(keikos)
            session.commit()
