from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from citadel.persistence.models import BaseUnitTable

if TYPE_CHECKING:
    from . import UnitTable


class ChronoUnitTable(BaseUnitTable):
    __tablename__ = "chrono_unit"

    seconds: Mapped[float] = mapped_column()

    unit: Mapped[UnitTable] = relationship(
        back_populates="chrono",
    )
