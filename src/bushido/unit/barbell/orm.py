from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bushido.unit.db_model import Subunit, UnitTable


class LiftingUnitTable(UnitTable):
    __tablename__ = "unit_lifting"

    subunits: Mapped[list["LiftingSet"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="unit",
    )


class LiftingSet(Subunit):
    __tablename__ = "lifting_set"

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    rest: Mapped[float] = mapped_column(default=0)
    fk_unit: Mapped[int] = mapped_column(ForeignKey(LiftingUnitTable.id))

    unit: Mapped[LiftingUnitTable] = relationship(
        back_populates="subunits",
    )
