from typing import Optional
from datetime import time
from sqlalchemy.orm import Mapped, mapped_column

# project imports
from bushido.data.base_models import AbsKeikoModel


class KeikoModel(AbsKeikoModel):
    __tablename__ = 'cardio'

    start_t: Mapped[time] = mapped_column()
    seconds: Mapped[float] = mapped_column()
    gym: Mapped[str] = mapped_column()
    distance: Mapped[Optional[float]] = mapped_column()
