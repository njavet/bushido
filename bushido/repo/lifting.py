from sqlalchemy.orm import Session

# project imports
from bushido.db import Exercise, LiftingSet
from bushido.repo.base import UnitRepo


class LiftingRepo(UnitRepo[Exercise, LiftingSet]):
    def __init__(self, session: Session):
        super().__init__(session)

    # TODO handle exceptions
    def add_unit(self, unit: Exercise, subunits: list[LiftingSet]) -> bool:
        self.session.add(unit)
        self.session.commit()
        for subunit in subunits:
            subunit.fk_exercise = unit.id
        self.session.add_all(subunits)
        self.session.commit()
        return True
