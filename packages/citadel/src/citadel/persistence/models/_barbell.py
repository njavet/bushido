from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, UnitTable


class BarbellUnitTable(UnitTable):
    __tablename__ = "barbell_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)
    variant: Mapped[str] = mapped_column(default="default")

    subunits: Mapped[list[BarbellSet]] = relationship(
        cascade="all, delete-orphan",
        back_populates="unit",
    )

    __mapper_args__ = {"polymorphic_identity": "barbell"}


class BarbellSet(Base):
    __tablename__ = "barbell_set"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    set_nr: Mapped[int] = mapped_column()
    rest: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    fk_unit: Mapped[int] = mapped_column(ForeignKey(BarbellUnitTable.id))

    unit: Mapped[BarbellUnitTable] = relationship(
        back_populates="subunits",
    )
