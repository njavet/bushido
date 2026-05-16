from sqlalchemy.orm import Session

from bushido.unit.repo import UnitRepo

from .orm import CardioUnitTable


class CardioRepo(UnitRepo[CardioUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, CardioUnitTable)
