from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

# project imports
from bushido.data.base_models import AbsKeikoModel


class KeikoModel(AbsKeikoModel):
    __tablename__ = 'log'

    log: Mapped[Optional[str]] = mapped_column()
