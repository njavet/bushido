from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from bushido.data.base_models import AbsKeikoModel
from bushido.data.base_repo import BaseRepository


class LogModel(AbsKeikoModel):
    __tablename__ = 'gym'

    log: Mapped[Optional[str]] = mapped_column()


class LogRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)
