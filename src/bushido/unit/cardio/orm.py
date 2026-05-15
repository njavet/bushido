import datetime

from sqlalchemy.orm import Mapped, mapped_column

from bushido.unit.db_model import UnitTable


class CardioUnitTable(UnitTable):
    __tablename__ = "cardio_unit"

    start_t: Mapped[datetime.time] = mapped_column()
    seconds: Mapped[float] = mapped_column()
    location: Mapped[str] = mapped_column()
    distance: Mapped[float | None] = mapped_column()
    avg_hr: Mapped[int | None] = mapped_column()
    max_hr: Mapped[int | None] = mapped_column()
    calories: Mapped[int | None] = mapped_column()
