import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ._base import BaseUnitTable


class MartialArtsUnitTable(BaseUnitTable):
    __tablename__ = "martial_arts_unit"

    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()
    gym: Mapped[str] = mapped_column()
