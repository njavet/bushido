from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# project imports
from ._base import Keiko


class Lifting(Keiko):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)

def create_keiko(attrs, unit_key) -> list:
    keikos = []
    for set_nr, w, r, p in attrs.zipped():
        lifting = Lifting(set_nr=set_nr,
                          weight=w,
                          reps=r,
                          pause=p,
                          unit=unit_key)
        keikos.append(lifting)
    return keikos
