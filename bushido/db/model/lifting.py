from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# project imports
from bushido.db.model.base import Base, Unit


class LiftingUnit(Unit):
    __tablename__ = 'unit_lifting'

    sets = relationship(
        back_populates='session',
        cascade='all, delete-orphan',
    )


class LiftingSet(Base):
    __tablename__ = 'lifting_set'

    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    rest: Mapped[float] = mapped_column(default=0)

    session = relationship(
        back_populates='sets',
    )
