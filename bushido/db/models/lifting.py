from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from bushido.db.models.base import Base, Keiko


class Lifting(Keiko):
    __tablename__ = 'lifting'


class LSet(Base):
    __tablename__ = 'lifting_set'
    set_nr: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    reps: Mapped[float] = mapped_column(nullable=False)
    pause: Mapped[int] = mapped_column()
    lifting: Mapped[int] = mapped_column(ForeignKey(Lifting.key),
                                         nullable=False)
