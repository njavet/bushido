from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from citadel.persistence.models import Base, UnitTable


class ChronoUnitTable(Base):
    __tablename__ = "chrono_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)
    seconds: Mapped[float] = mapped_column()
