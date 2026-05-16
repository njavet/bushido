import datetime

from sqlalchemy.orm import Mapped, mapped_column

from bushido.units.db_model import UnitTable


class MartialArtsUnitTable(UnitTable):
    __tablename__ = "martial_arts_unit"

    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    gym: Mapped[str] = mapped_column()
    sensei: Mapped[str | None] = mapped_column()
    training: Mapped[str | None] = mapped_column()
    focus: Mapped[str | None] = mapped_column()
