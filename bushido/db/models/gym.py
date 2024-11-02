from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from bushido.db.models.base import Keiko


class Gym(Keiko):
    __tablename__ = 'gym'

    start_t: Mapped[float] = mapped_column(nullable=False)
    end_t: Mapped[float] = mapped_column(nullable=False)
    gym: Mapped[str] = mapped_column(nullable=False)
    training: Mapped[str] = mapped_column()
