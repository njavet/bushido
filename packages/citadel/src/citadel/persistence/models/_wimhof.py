from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, UnitTable


class WimhofUnitTable(UnitTable):
    __tablename__ = "wimhof_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)

    zen_mode: Mapped[bool] = mapped_column()
    guide: Mapped[str | None] = mapped_column()

    subunits: Mapped[list[WimhofRound]] = relationship(
        cascade="all, delete-orphan",
        back_populates="unit",
    )

    __mapper_args__ = {"polymorphic_identity": "wimhof"}


class WimhofRound(Base):
    __tablename__ = "wimhof_round"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()
    fk_unit: Mapped[int] = mapped_column(ForeignKey(WimhofUnitTable.id))

    unit: Mapped[WimhofUnitTable] = relationship(
        back_populates="subunits",
    )
