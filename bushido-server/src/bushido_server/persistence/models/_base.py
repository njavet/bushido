import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from bushidolib.constants import UnitCategory


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Spartan(Base):
    __tablename__ = "spartan"

    name: Mapped[str] = mapped_column(unique=True)
    height: Mapped[int | None] = mapped_column()
    deployment_date: Mapped[datetime.date | None] = mapped_column()


class UnitConfigTable(Base):
    __tablename__ = "unit_config"

    name: Mapped[str] = mapped_column(unique=True)
    category: Mapped[UnitCategory] = mapped_column()


class UnitTable(Base):
    __abstract__ = True

    comment: Mapped[str | None] = mapped_column()
    log_time: Mapped[datetime.datetime] = mapped_column()

    unit_config_id: Mapped[int] = mapped_column(ForeignKey(UnitConfigTable.id))
