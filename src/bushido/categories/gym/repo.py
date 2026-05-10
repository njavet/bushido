from sqlalchemy.orm import Session

from bushido.core.repo import UnitRepo

from .orm import GymUnitTable


class GymRepo(UnitRepo[GymUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, GymUnitTable)
