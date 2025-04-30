from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from bushido.data.base_models import AbsKeikoModel
from bushido.data.base_repo import BaseRepository


class ChronoModel(AbsKeikoModel):
    __tablename__ = 'chrono'

    seconds: Mapped[float] = mapped_column()


class ChronoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)
