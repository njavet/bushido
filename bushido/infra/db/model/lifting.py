from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bushido.infra.db.model.base import Unit, Subunit


class LiftingUnit(Unit):
    __tablename__ = 'lifting_unit'

    sets: Mapped[list['LiftingSet']] = relationship(
        cascade='all, delete-orphan',
        back_populates='unit',
    )


class LiftingSet(Subunit):
    __tablename__ = 'lifting_set'

    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    rest: Mapped[float] = mapped_column(default=0)
    fk_unit: Mapped[int] = mapped_column(ForeignKey(LiftingUnit.id))

    unit: Mapped[Unit] = relationship(
        back_populates='sets',
    )
