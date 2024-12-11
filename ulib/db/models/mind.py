from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional

# project imports
from .base import Keiko


class Mind(Keiko):
    __tablename__ = 'mind'

    seconds: Mapped[float] = mapped_column()
    start_t: Mapped[Optional[float]] = mapped_column()
    end_t: Mapped[Optional[float]] = mapped_column()
    breaks: Mapped[Optional[float]] = mapped_column()
    project: Mapped[str] = mapped_column()
    topic: Mapped[str] = mapped_column()

