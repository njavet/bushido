import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ._base import UnitTable


class LiftingUnitTable(UnitTable):
    __tablename__ = "lifting_unit"

    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    gym: Mapped[str] = mapped_column()
