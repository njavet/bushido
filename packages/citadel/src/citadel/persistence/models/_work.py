import datetime
from typing import Any, ClassVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import UnitTable


class WorkUnitTable(UnitTable):
    __tablename__ = "work_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)

    start_t: Mapped[datetime.time | None] = mapped_column()
    end_t: Mapped[datetime.time | None] = mapped_column()
    seconds: Mapped[float | None] = mapped_column()
    gym: Mapped[str] = mapped_column()
    project: Mapped[str] = mapped_column()
    topic: Mapped[str] = mapped_column()

    __mapper_args__: ClassVar[dict[str, Any]] = {"polymorphic_identity": "work"}
