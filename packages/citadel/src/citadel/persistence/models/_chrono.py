from sqlalchemy.orm import Mapped, mapped_column

from citadel.persistence.models import UnitTable


class ChronoUnitTable(UnitTable):
    __tablename__ = "chrono_unit"

    name: Mapped[str] = mapped_column()
    seconds: Mapped[float] = mapped_column()
