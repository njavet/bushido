from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from bushido.db.models.base import Keiko
from bushido.db.models import GymName


class Cardio(Keiko):
    __tablename__ = 'cardio'
    start_t: Mapped[float] = mapped_column(nullable=False)
    seconds: Mapped[float] = mapped_column(nullable=False)

    distance: Mapped[float] = mapped_column()
    cal: Mapped[int] = mapped_column()
    avghr: Mapped[int] = mapped_column()
    maxhr: Mapped[int] = mapped_column()

    gym: Mapped[str] = mapped_column(ForeignKey(GymName.name),
                                     nullable=False)
