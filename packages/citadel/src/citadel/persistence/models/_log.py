from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from citadel.persistence.models._base import BaseUnitTable

if TYPE_CHECKING:
    from . import UnitTable


class LogUnitTable(BaseUnitTable):
    __tablename__ = "log_unit"

    kind: Mapped[str] = mapped_column()
    unit: Mapped[UnitTable] = relationship(
        back_populates="log",
    )
