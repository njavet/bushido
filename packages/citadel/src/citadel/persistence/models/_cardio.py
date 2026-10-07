import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import BaseUnitTable

if TYPE_CHECKING:
    from . import UnitTable


class CardioUnitTable(BaseUnitTable):
    __abstract__ = True

    start_t: Mapped[datetime.time] = mapped_column()
    seconds: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()
    avg_hr: Mapped[int | None] = mapped_column()
    max_hr: Mapped[int | None] = mapped_column()
    calories: Mapped[int | None] = mapped_column()


class RunningUnitTable(CardioUnitTable):
    __tablename__ = "running_unit"

    distance: Mapped[float] = mapped_column()
    unit: Mapped[UnitTable] = relationship(
        back_populates="running",
    )


class SwimmingUnitTable(CardioUnitTable):
    __tablename__ = "swimming_unit"

    distance: Mapped[float] = mapped_column()
    pool_length: Mapped[int | None] = mapped_column()
    temperature: Mapped[float | None] = mapped_column()
    unit: Mapped[UnitTable] = relationship(
        back_populates="swimming",
    )


class RopeSkipUnitTable(CardioUnitTable):
    __tablename__ = "rope_skip_unit"
    unit: Mapped[UnitTable] = relationship(
        back_populates="skipping",
    )
