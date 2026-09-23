import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ._base import UnitTable


class CaliUnitTable(UnitTable):
    __tablename__ = "cali_unit"

    pushups: Mapped[int] = mapped_column()
    squats: Mapped[int] = mapped_column()
    situps: Mapped[int] = mapped_column()
    pullups: Mapped[int] = mapped_column()
