from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from citadel.persistence.models import Base, BaseUnitTable


class ChronoUnitTable(BaseUnitTable):
    __tablename__ = "chrono_unit"

    seconds: Mapped[float] = mapped_column()
