from typing import Any, ClassVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import UnitTable


class ChronoUnitTable(UnitTable):
    __tablename__ = "chrono_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)

    seconds: Mapped[float] = mapped_column()

    __mapper_args__: ClassVar[dict[str, Any]] = {"polymorphic_identity": "chrono"}
