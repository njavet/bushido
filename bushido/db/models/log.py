from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional

# project imports
from bushido.db.models.base import Keiko


class Log(Keiko):
    __tablename__ = 'log'

    log: Mapped[Optional[str]] = mapped_column()
