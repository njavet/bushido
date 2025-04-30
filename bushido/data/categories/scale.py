from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from bushido.data.base_models import AbsKeikoModel
from bushido.data.base_repo import BaseRepository


class ScaleModel(AbsKeikoModel):
    __tablename__ = 'scale'

    weight: Mapped[float] = mapped_column()
    belly: Mapped[float] = mapped_column()


class ScaleRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)
