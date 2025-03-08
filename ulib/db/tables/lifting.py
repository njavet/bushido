from sqlalchemy.orm import Mapped, mapped_column

# project imports
from ulib.db.tables.base import KeikoTable


class LiftingTable(KeikoTable):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)
