from sqlalchemy.orm import Mapped, mapped_column

from citadel.persistence.models import UnitTable


class LogUnitTable(UnitTable):
    __tablename__ = "log_unit"

    name: Mapped[str] = mapped_column()
    kind: Mapped[str] = mapped_column()
