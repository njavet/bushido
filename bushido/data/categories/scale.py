from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped

# project imports
from bushido.data.base_tables import AbsKeikoTable


def create_keiko_orm(keiko_spec):
    keiko = KeikoTable(weight=keiko_spec.weight,
                       belly=keiko_spec.belly)
    return keiko


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'scale'

    weight: Mapped[float] = mapped_column()
    belly: Mapped[Optional[float]] = mapped_column()
