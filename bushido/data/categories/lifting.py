from sqlalchemy.orm import Mapped, mapped_column

# project imports
from bushido.data.base_models import AbsKeikoModel


class KeikoModel(AbsKeikoModel):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)
