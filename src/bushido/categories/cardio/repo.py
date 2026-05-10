from sqlalchemy.orm import Session

from ..repo import UnitRepo
from .orm import CardioUnitTable


class GymRepo(UnitRepo[CardioUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, CardioUnitTable)
