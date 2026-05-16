from sqlalchemy.orm import Session

from bushido.units.repo import UnitRepo

from .db_model import RunningUnitTable


class RunningRepo(UnitRepo[RunningUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, RunningUnitTable)
