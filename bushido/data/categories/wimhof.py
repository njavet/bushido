from sqlalchemy.orm import Mapped, mapped_column

# project imports
from bushido.data.base_tables import AbsKeikoTable


def create_keiko_orm(keiko_spec):
    keikos = []
    for round_nr, (b, r) in enumerate(zip(keiko_spec.breaths, keiko_spec.retentions)):
        keiko = KeikoTable(round_nr=round_nr,
                           breaths=b,
                           retention=r)
        keikos.append(keiko)
    return keikos


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'wimhof'

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()
