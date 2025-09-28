import datetime

from sqlalchemy.orm import Mapped, mapped_column

from bushido.infra.db.model.base import Unit


class GymUnit(Unit):
    __tablename__ = 'gym_unit'

    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    location: Mapped[str] = mapped_column()
    focus: Mapped[str | None] = mapped_column()
