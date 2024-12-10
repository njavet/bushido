from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from bushido.db.models.base import Keiko


class Log(Keiko):
    __tablename__ = 'log'

    log: Mapped[str] = mapped_column()

