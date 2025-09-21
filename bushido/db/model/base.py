from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Unit(Base):
    __abstract__ = True


class Subunit(Base):
    __abstract__ = True
    fk_unit: Mapped[int] = mapped_column(ForeignKey(Unit.id))
