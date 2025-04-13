from sqlalchemy.orm import Mapped, mapped_column

# project imports
from bushido.data.base_tables import AbsKeikoTable


def create_keiko_orm(keiko_spec):
    keikos = []
    for set_nr, (w, r, p) in enumerate(zip(keiko_spec.weights,
                                           keiko_spec.reps,
                                           keiko_spec.pauses)):
        keiko = KeikoTable(set_nr=set_nr,
                           weight=w,
                           reps=r,
                           pause=p)
        keikos.append(keiko)
    return keikos


class KeikoTable(AbsKeikoTable):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)
