from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from bushido.data.base_models import AbsKeikoModel


class ScaleModel(AbsKeikoModel):
    __tablename__ = 'scale'

    weight: Mapped[float] = mapped_column()
    belly: Mapped[Optional[float]] = mapped_column()
