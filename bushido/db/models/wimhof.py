from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from bushido.db.models.base import Base, Keiko


class Wimhof(Keiko):
    __tablename__ = 'wimhof'


class WimhofRound(Base):
    __tablename__ = 'rounds'

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()
    wimhof: Mapped[int] = mapped_column(ForeignKey(Wimhof.key))

