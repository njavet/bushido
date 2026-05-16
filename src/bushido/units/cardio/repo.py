from sqlalchemy.orm import Session

from bushido.db.model.cardio import CardioUnitTable
from bushido.db.repo.base import UnitRepo


class CardioRepo(UnitRepo[CardioUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, CardioUnitTable)
