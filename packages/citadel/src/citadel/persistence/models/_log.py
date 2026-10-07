from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from citadel.persistence.models import Base, UnitTable

class LogUnitTable(Base):
    __tablename__ = "log_unit"

    id: Mapped[int] = mapped_column(ForeignKey(UnitTable.id), primary_key=True)
    kind: Mapped[str] = mapped_column()
