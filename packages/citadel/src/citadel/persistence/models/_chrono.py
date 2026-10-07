from sqlalchemy.orm import Mapped, mapped_column

from citadel.persistence.models import BaseUnitTable


class ChronoUnitTable(BaseUnitTable):
    __tablename__ = "chrono_unit"

    seconds: Mapped[float] = mapped_column()
