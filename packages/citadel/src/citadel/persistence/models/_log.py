from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from citadel.persistence.models import Base, UnitTable
from citadel.persistence.models._base import BaseUnitTable


class LogUnitTable(BaseUnitTable):
    __tablename__ = "log_unit"

    kind: Mapped[str] = mapped_column()
