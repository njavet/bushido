from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from bushido.db.models.base import Keiko


class Chrono(Keiko):
    __tablename__ = 'chrono'

    seconds: Mapped[float] = mapped_column()

