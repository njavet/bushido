from sqlalchemy.orm import Mapped, mapped_column, Session
from bushido.data.base_models import AbsKeikoModel
from bushido.data.base_repo import BaseRepository


class WimhofModel(AbsKeikoModel):
    __tablename__ = 'wimhof'

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()


class WimhofRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)
