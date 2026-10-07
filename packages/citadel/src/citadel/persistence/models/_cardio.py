import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base, UnitTable


class CardioUnitTable(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)
    start_t: Mapped[datetime.time] = mapped_column()
    seconds: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()
    avg_hr: Mapped[int | None] = mapped_column()
    max_hr: Mapped[int | None] = mapped_column()
    calories: Mapped[int | None] = mapped_column()


class RunningUnitTable(CardioUnitTable):
    __tablename__ = "running_unit"

    distance: Mapped[float] = mapped_column()


class SwimmingUnitTable(CardioUnitTable):
    __tablename__ = "swimming_unit"

    distance: Mapped[float] = mapped_column()
    pool_length: Mapped[int | None] = mapped_column()
    temperature: Mapped[float | None] = mapped_column()


class RopeSkipUnitTable(CardioUnitTable):
    __tablename__ = "rope_skip_unit"
