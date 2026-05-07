import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ..orm import UnitTable


class GymUnitTable(UnitTable):
    __tablename__ = "gym_unit"

    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    gym: Mapped[str] = mapped_column()
    intensity: Mapped[int] = mapped_column()
    training: Mapped[str | None] = mapped_column()
    focus: Mapped[str | None] = mapped_column()
    private: Mapped[bool] = mapped_column()
