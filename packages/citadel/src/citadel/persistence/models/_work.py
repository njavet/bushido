import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base, BaseUnitTable, UnitTable


class WorkUnitTable(BaseUnitTable):
    __tablename__ = "work_unit"

    start_t: Mapped[datetime.time | None] = mapped_column()
    end_t: Mapped[datetime.time | None] = mapped_column()
    seconds: Mapped[float | None] = mapped_column()
    gym: Mapped[str] = mapped_column()
    project: Mapped[str] = mapped_column()
    topic: Mapped[str] = mapped_column()
