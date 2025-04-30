from typing import Optional
from datetime import time
from sqlalchemy.orm import Mapped, mapped_column

# project imports
from bushido.data.base_models import AbsKeikoModel


class KeikoModel(AbsKeikoModel):
    __tablename__ = 'gym'

    start_t: Mapped[time] = mapped_column()
    end_t: Mapped[time] = mapped_column()
    gym: Mapped[Optional[str]] = mapped_column()
