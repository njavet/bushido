from sqlalchemy.orm import mapped_column, Mapped

# project imports
from ulib.db.tables.base import KeikoTable


class GymTable(KeikoTable):
    __tablename__ = 'gym'

    start_t: Mapped[float] = mapped_column()
    end_t: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()
