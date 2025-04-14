from sqlalchemy.orm import Mapped, mapped_column, Session
from bushido.data.base_models import AbsKeikoModel
from bushido.data.unit import UnitRepository


class GymModel(AbsKeikoModel):
    __tablename__ = 'gym'

    start_t: Mapped[int] = mapped_column()
    end_t: Mapped[int] = mapped_column()
    gym: Mapped[str] = mapped_column()


class GymRepository(UnitRepository):
    def __init__(self, session: Session):
        super().__init__(session)
