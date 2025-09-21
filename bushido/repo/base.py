from typing import Sequence
from sqlalchemy.orm import Session

# project imports
from bushido.core.types import ORM_T, ORM_ST


class UnitRepo:
    def __init__(self, session: Session):
        self.session = session

    # TODO handle exceptions
    def add_unit(self, unit: ORM_T, subunits: Sequence[ORM_ST]) -> bool:
        self.session.add(unit)
        self.session.commit()
        for subunit in subunits:
            subunit.fk_unit = unit.id
        self.session.add_all(subunits)
        self.session.commit()
        return True
