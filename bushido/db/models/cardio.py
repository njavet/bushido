from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional

# project imports
from bushido.db.models.base import Keiko


class Cardio(Keiko):
    __tablename__ = 'cardio'
    start_t: Mapped[float] = mapped_column(nullable=False)
    seconds: Mapped[float] = mapped_column(nullable=False)

    distance: Mapped[Optional[float]] = mapped_column()
    cal: Mapped[Optional[int]] = mapped_column()
    avghr: Mapped[Optional[int]] = mapped_column()
    maxhr: Mapped[Optional[int]] = mapped_column()

    gym: Mapped[str] = mapped_column(nullable=False)
