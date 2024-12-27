from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from .base import Keiko, UploaderFactory


class Lifting(Keiko):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)


class Uploader(UploaderFactory):
    def __init__(self, engine):
        super().__init__(engine)

    def upload_keiko(self, attrs):
        keikos = []
        for set_nr, w, r, p in attrs.zipped():
            lifting = Lifting(set_nr=set_nr,
                              weight=w,
                              reps=r,
                              pause=p,
                              unit=self.unit.key)
            keikos.append(lifting)

        with Session(self.engine) as session:
            session.add_all(keikos)
            session.commit()
