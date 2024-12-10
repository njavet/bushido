from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional

# project imports
from bushido.db.models.base import Keiko


class Scale(Keiko):
    __tablename__ = 'scale'

    weight: Mapped[float] = mapped_column()
    fat: Mapped[Optional[float]] = mapped_column()
    water: Mapped[Optional[float]] = mapped_column()
    muscles: Mapped[Optional[float]] = mapped_column()
