from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from base_tables import Keiko


class Log(Keiko):
    __tablename__ = 'log'
    log: Mapped[str] = mapped_column(nullable=False)

