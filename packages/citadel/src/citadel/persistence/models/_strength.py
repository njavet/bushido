import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, UnitTable


class StrengthUnitTable(UnitTable):
    __tablename__ = "strength_unit"

    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    gym: Mapped[str] = mapped_column()


class LiftingUnitTable(UnitTable):
    __tablename__ = "lifting_unit"

    exercise: Mapped[str] = mapped_column()
    variant: Mapped[str] = mapped_column(default="default")
    subunits: Mapped[list[LiftingSet]] = relationship(
        cascade="all, delete-orphan",
        back_populates="unit",
    )


class LiftingSet(Base):
    __tablename__ = "lifting_set"

    set_nr: Mapped[int] = mapped_column()
    rest: Mapped[float] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    fk_unit: Mapped[int] = mapped_column(ForeignKey(LiftingUnitTable.id))

    unit: Mapped[LiftingUnitTable] = relationship(
        back_populates="subunits",
    )
