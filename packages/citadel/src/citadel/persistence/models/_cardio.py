import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import UnitTable


class CardioUnitTable(UnitTable):
    __abstract__ = True

    start_t: Mapped[datetime.time] = mapped_column()
    seconds: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()
    avg_hr: Mapped[int | None] = mapped_column()
    max_hr: Mapped[int | None] = mapped_column()
    calories: Mapped[int | None] = mapped_column()


class RunningUnitTable(CardioUnitTable):
    __tablename__ = "running_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)
    distance: Mapped[float] = mapped_column()

    __mapper_args__ = {"polymorphic_identity": "running"}


class SwimmingUnitTable(CardioUnitTable):
    __tablename__ = "swimming_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)
    distance: Mapped[float] = mapped_column()
    pool_length: Mapped[int | None] = mapped_column()
    temperature: Mapped[float | None] = mapped_column()

    __mapper_args__ = {"polymorphic_identity": "swimming"}


class RopeSkipUnitTable(CardioUnitTable):
    __tablename__ = "skipping_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "skipping"}
