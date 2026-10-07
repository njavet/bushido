from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, BaseUnitTable

if TYPE_CHECKING:
    from . import UnitTable


class BarbellUnitTable(BaseUnitTable):
    __tablename__ = "barbell_unit"

    variant: Mapped[str] = mapped_column(default="default")
    unit: Mapped[UnitTable] = relationship(
        back_populates="barbell",
    )
    subunits: Mapped[list[BarbellSet]] = relationship(
        cascade="all, delete-orphan",
        back_populates="unit",
    )


class BarbellSet(Base):
    __tablename__ = "barbell_set"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    set_nr: Mapped[int] = mapped_column()
    rest: Mapped[float] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    fk_unit: Mapped[int] = mapped_column(ForeignKey(BarbellUnitTable.id))

    unit: Mapped[BarbellUnitTable] = relationship(
        back_populates="subunits",
    )
