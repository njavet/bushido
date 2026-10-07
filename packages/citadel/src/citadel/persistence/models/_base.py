from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

if TYPE_CHECKING:
    pass


class Base(DeclarativeBase):
    pass


class BaseUnitTable(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(ForeignKey("unit.id"), primary_key=True)
