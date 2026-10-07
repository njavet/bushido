from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from citadel.persistence.models import UnitTable


class ChronoUnitTable(UnitTable):
    __tablename__ = "chrono_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)

    seconds: Mapped[float] = mapped_column()

    __mapper_args__ = {"polymorphic_identity": "chrono"}
