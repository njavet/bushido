from sqlalchemy.orm import Mapped, mapped_column, Session
from bushido.data.base_models import AbsKeikoModel
from bushido.data.unit import UnitRepository


class LiftingModel(AbsKeikoModel):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)


class LiftingRepository(UnitRepository):
    def __init__(self, session: Session):
        super().__init__(session)
