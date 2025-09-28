from typing import Sequence, Generic, TypeVar, Protocol

from sqlalchemy.orm import Session, Mapped


class Unit(Protocol):
    id: int


class CompoundUnit(Protocol):
    id: int


class Subunit(Protocol):
    id: int
    fk_unit: int


UT_ORM = TypeVar('UT_ORM', bound=Unit)
CUT_ORM = TypeVar('CUT_ORM', bound=CompoundUnit)
SUT_ORM = TypeVar('SUT_ORM', bound=Subunit)


class UnitRepo(Generic[UT_ORM]):
    def __init__(self, session: Session) -> None:
        self.session = session

    # TODO handle exceptions
    def add_unit(self, unit: UT_ORM) -> bool:
        self.session.add(unit)
        self.session.commit()
        return True


class CompoundUnitRepo(Generic[CUT_ORM, SUT_ORM]):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_compound_unit(
        self, unit: CUT_ORM, subunits: Sequence[SUT_ORM]
    ) -> bool:
        self.session.add(unit)
        self.session.commit()
        for subunit in subunits:
            subunit.fk_unit = unit.id
        self.session.add_all(subunits)
        self.session.commit()
        return True
