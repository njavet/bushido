from sqlalchemy.orm import mapped_column, Mapped, Session
from typing import Optional

# project imports
from ulib.db.base import Keiko, BaseUploader


class Gym(Keiko):
    __tablename__ = 'gym'

    start_t: Mapped[float] = mapped_column()
    end_t: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()
    training: Mapped[Optional[str]] = mapped_column()


class GymUploader(BaseUploader):
    def __init__(self, engine):
        super().__init__(engine)

    def upload_keiko(self, attrs):
        keiko = Gym(start_t=attrs.start_t,
                    end_t=attrs.end_t,
                    gym=attrs.gym,
                    training=attrs.training,
                    unit=self.unit.key)
        with Session(self.engine) as session:
            session.add(keiko)
            session.commit()
