from sqlalchemy.orm import Session

from bushido.db.model.gym import GymUnitTable
from bushido.units.repo import UnitRepo


class GymRepo(UnitRepo[GymUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, GymUnitTable)
