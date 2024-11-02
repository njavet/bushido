from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from bushido.db.models.base import Keiko


class Mind(Keiko):
    __tablename__ = 'mind'

    seconds: Mapped[float] = mapped_column(nullable=False)
    start_t: Mapped[float] = mapped_column()
    end_t: Mapped[float] = mapped_column()
    breaks: Mapped[int] = mapped_column()

    project: Mapped[str] = mapped_column(nullable=False)
    topic: Mapped[str] = mapped_column(nullable=False)
