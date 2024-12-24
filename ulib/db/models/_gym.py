from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional

# project imports
from ._base import Keiko


class Gym(Keiko):
    __tablename__ = 'gym'

    start_t: Mapped[float] = mapped_column()
    end_t: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()
    training: Mapped[Optional[str]] = mapped_column()

