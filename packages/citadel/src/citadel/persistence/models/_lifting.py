import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import BaseUnitTable

if TYPE_CHECKING:
    from . import UnitTable


class LiftingUnitTable(BaseUnitTable):
    __tablename__ = "lifting_unit"

    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    gym: Mapped[str] = mapped_column()
    unit: Mapped[UnitTable] = relationship(
        back_populates="lifting",
    )
