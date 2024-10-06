from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from base_tables import Base, Keiko


class Wimhof(Keiko):
    __tablename__ = 'wimhof'


class WimhofRound(Base):
    __tablename__ = 'rounds'
    round_nr: Mapped[int] = mapped_column(nullable=False)
    breaths: Mapped[int] = mapped_column(nullable=False)
    retention: Mapped[int] = mapped_column(nullable=False)
    wimhof: Mapped[int] = mapped_column(ForeignKey(Wimhof.id_),
                                        nullable=False)
