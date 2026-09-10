import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ._base import UnitTable


class GymUnitTable(UnitTable):
    __tablename__ = "gym_unit"

    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    gym: Mapped[str] = mapped_column()
