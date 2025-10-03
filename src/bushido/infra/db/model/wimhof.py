from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bushido.infra.db.model.base import Base, Unit


class WimhofUnit(Unit):
    __tablename__ = 'wimhof_unit'

    subunits: Mapped[list['WimhofRound']] = relationship(
        cascade='all, delete-orphan',
        back_populates='unit',
    )


class WimhofRound(Base):
    __tablename__ = 'wimhof_round'

    id: Mapped[int] = mapped_column(primary_key=True)
    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()
    fk_unit: Mapped[int] = mapped_column(ForeignKey(WimhofUnit.id))

    unit: Mapped[WimhofUnit] = relationship(
        back_populates='subunits',
    )
