from sqlalchemy.orm import Session

from bushido.units.repo import UnitRepo

from .db_model import LiftingUnitTable


class LiftingRepo(UnitRepo[LiftingUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, LiftingUnitTable)
