from typing import Sequence, Protocol, TypeVar

from sqlalchemy.orm import Session


UNIT_ORM_T = TypeVar("UNIT_ORM_T")
SUB_ORM_T = TypeVar("SUB_ORM_T")


class UnitRepo(Protocol[UNIT_ORM_T]):
    def __init__(self, session: Session) -> None:
        self.session = session

    # TODO handle exceptions
    def add_unit(self, unit: UNIT_ORM_T) -> bool:
        self.session.add(unit)
        self.session.commit()
        return True


class CompoundUnitRepo(Protocol[UNIT_ORM_T, SUB_ORM_T]):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_compound_unit(
        self, unit: UNIT_ORM_T, subunits: Sequence[SUB_ORM_T]
    ) -> bool:
        unit.subunits.extend(subunits)
        self.session.add(unit)
        self.session.commit()
        return True
