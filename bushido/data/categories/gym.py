from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped


# project imports
from bushido.data.base_tables import AbsKeikoTable


def create_keiko_orm(keiko_spce):
    keiko_orm = KeikoTable(start_t=keiko_spce.start_t,
                           end_t=keiko_spce.end_t,
                           gym=keiko_spce.gym)
    return keiko_orm


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'gym'

    start_t: Mapped[int] = mapped_column(BigInteger)
    end_t: Mapped[int] = mapped_column(BigInteger)
    gym: Mapped[str] = mapped_column()
