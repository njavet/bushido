from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import UnitTable


class LogUnitTable(UnitTable):
    __tablename__ = "log_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)

    kind: Mapped[str] = mapped_column()
    unit: Mapped[UnitTable] = relationship(
        back_populates="log",
    )

    __mapper_args__ = {"polymorphic_identity": "log"}
