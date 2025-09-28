from typing import Generic, Protocol, TypeVar

from sqlalchemy.orm import Session


class Unit(Protocol):
    id: int


class Subunit(Protocol):
    id: int
    fk_unit: int


U = TypeVar('U', bound=Unit)
S = TypeVar('S', bound=Subunit)


class UnitRepo(Generic[U, S]):
    def __init__(self, session: Session) -> None:
        self.session = session

    # TODO handle exceptions
    def add_unit(self, unit: U, subs: list[S] | None = None) -> bool:
        subs = subs or []
        self.session.add(unit)
        self.session.commit()
        for subunit in subs:
            subunit.fk_unit = unit.id
        self.session.add_all(subs)
        self.session.commit()
        return True
