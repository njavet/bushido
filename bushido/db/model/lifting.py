from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bushido.db.model.base import Subunit, Unit


class LiftingUnit(Unit):
    __tablename__ = 'lifting'

    sets: Mapped[list['LiftingSet']] = relationship(
        back_populates='exercise',
        cascade='all, delete-orphan',
    )


class LiftingSet(Subunit):
    __tablename__ = 'lifting_set'

    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    rest: Mapped[float] = mapped_column(default=0)

    fk_unit: Mapped[int] = mapped_column(ForeignKey(LiftingUnit.id))

    exercise: Mapped[LiftingUnit] = relationship(
        back_populates='sets',
    )
