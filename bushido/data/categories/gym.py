from typing import Optional
from datetime import time
from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from bushido.data.base_models import AbsKeikoModel
from bushido.data.base_repo import BaseRepository


class KeikoModel(AbsKeikoModel):
    __tablename__ = 'gym'

    start_t: Mapped[time] = mapped_column()
    end_t: Mapped[time] = mapped_column()
    gym: Mapped[Optional[str]] = mapped_column()


class Repository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)
