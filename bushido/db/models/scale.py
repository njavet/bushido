from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from bushido.db.models.base import Keiko


class Scale(Keiko):
    __tablename__ = 'scale'
    weight: Mapped[float] = mapped_column(nullable=False)
    fat: Mapped[float] = mapped_column()
    water: Mapped[float] = mapped_column()
    muscles: Mapped[float] = mapped_column()
