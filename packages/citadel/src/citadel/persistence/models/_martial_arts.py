import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ._base import UnitTable


class MartialArtsUnitTable(UnitTable):
    __tablename__ = "martial_arts_unit"

    kind: Mapped[str] = mapped_column()
    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    gym: Mapped[str] = mapped_column()
