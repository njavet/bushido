from sqlalchemy.orm import Mapped, mapped_column
from bushido.data.models import AbsKeikoTable
from bushido.data.unit import UnitRepository


class GymModel(AbsKeikoTable):
    __tablename__ = 'gym'

    start_t: Mapped[int] = mapped_column()
    end_t: Mapped[int] = mapped_column()
    gym: Mapped[str] = mapped_column()


class GymRepository(UnitRepository):