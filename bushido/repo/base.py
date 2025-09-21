from typing import Any
from sqlalchemy.orm import Session

# project imports


class UnitRepo:
    def __init__(self, session: Session):
        self.session = session

    # TODO handle exceptions
    def add_unit(self, unit: Any, subunits: Any) -> bool:
        self.session.add(unit)
        self.session.commit()
        for subunit in subunits:
            subunit.fk_unit = unit.id
        self.session.add_all(subunits)
        self.session.commit()
        return True
