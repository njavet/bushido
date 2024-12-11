from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from .base import Keiko


class Lifting(Keiko):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)
