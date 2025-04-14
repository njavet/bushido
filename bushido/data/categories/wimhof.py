from sqlalchemy.orm import Mapped, mapped_column
from bushido.data.base_models import AbsKeikoModel


class WimhofModel(AbsKeikoModel):
    __tablename__ = 'wimhof'

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()
