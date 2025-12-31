import datetime

from sqlalchemy.orm import Mapped, mapped_column

from bushido.modules.orm import Unit


class CardioUnit(Unit):
    __tablename__ = "cardio_unit"

    kind: Mapped[str] = mapped_column()
    start_t: Mapped[datetime.time] = mapped_column()
    seconds: Mapped[float] = mapped_column()
    location: Mapped[str] = mapped_column()
    distance: Mapped[float | None] = mapped_column()
    avg_hr: Mapped[int | None] = mapped_column()
    max_hr: Mapped[int | None] = mapped_column()
    calories: Mapped[int | None] = mapped_column()
