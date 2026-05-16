from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bushido.db.model.base import Base, UnitTable


class WimhofUnitTable(UnitTable):
    __tablename__ = "wimhof_unit"

    rounds: Mapped[list["WimhofRound"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="unit",
    )


class WimhofRound(Base):
    __tablename__ = "wimhof_round"

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()
    fk_unit: Mapped[int] = mapped_column(ForeignKey(WimhofUnitTable.id))

    unit: Mapped[WimhofUnitTable] = relationship(
        back_populates="rounds",
    )
