from sqlalchemy.orm import Mapped, mapped_column, relationship

# project imports
from bushido.db.model.base import Base


class LiftingSet(Base):
    __tablename__ = 'lifting_set'

    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    rest: Mapped[float] = mapped_column(default=0)

    exercise = relationship('Exercise', back_populates='lifting_sets')


class Exercise(Base):
    __tablename__ = 'exercise'

    name: Mapped[str] = mapped_column()
    sets: list[LiftingSet] = mapped_column()

    lifting_sets = relationship('LiftingSet', back_populates='exercise')
