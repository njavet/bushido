from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db_model import UnitTable, Base


class BarbellUnitTable(UnitTable):
    __tablename__ = "barbell_unit"

    sets: Mapped[list["BarbellSet"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="barbell_set",
    )


class BarbellSet(Base):
    __tablename__ = "barbell_set"

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    rest: Mapped[float] = mapped_column(default=0)
    fk_unit: Mapped[int] = mapped_column(ForeignKey(BarbellUnitTable.id))

    unit: Mapped[BarbellUnitTable] = relationship(
        back_populates="sets",
    )
