from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from .base import Keiko


class Wimhof(Keiko):
    __tablename__ = 'wimhof'

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()
