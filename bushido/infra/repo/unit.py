from typing import Sequence

from sqlalchemy.orm import Session

from bushido.core.types import ORM_T
from bushido.infra.db import Unit


class UnitRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    # TODO handle exceptions
    def add_unit(self, unit: Unit, subunits: Sequence[ORM_T]) -> bool:
        self.session.add(unit)
        self.session.commit()
        for subunit in subunits:
            subunit.fk_unit = unit.id
        self.session.add_all(subunits)
        self.session.commit()
        return True
