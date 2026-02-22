import datetime

from sqlalchemy.orm import Mapped, mapped_column

from bushido.units.orm import Unit


class WorkUnit(Unit):
    __tablename__ = "work_unit"

    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    location: Mapped[str] = mapped_column()
    employer: Mapped[str] = mapped_column()
    project: Mapped[str] = mapped_column()
