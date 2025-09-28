from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bushido.infra.db.model.base import Base, Unit


class LiftingUnit(Unit):
    __tablename__ = 'lifting_unit'

    subunits: Mapped[list['LiftingSet']] = relationship(
        cascade='all, delete-orphan',
        back_populates='unit',
    )


class LiftingSet(Base):
    __tablename__ = 'lifting_set'

    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    rest: Mapped[float] = mapped_column(default=0)
    fk_unit: Mapped[int] = mapped_column(ForeignKey(LiftingUnit.id))

    unit: Mapped[Unit] = relationship(
        back_populates='subunits',
    )
