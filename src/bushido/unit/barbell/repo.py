import datetime

from sqlalchemy.orm import Session, selectinload

from ..repo import UnitRepo
from .db_model import BarbellUnitTable


class LiftingRepo(UnitRepo[BarbellUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, BarbellUnitTable)

    def fetch_units(
        self,
        unit_name: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[BarbellUnitTable]:
        return self._fetch_units(
            unit_name=unit_name,
            start_t=start_t,
            end_t=end_t,
            options=[selectinload(BarbellUnitTable.sets)],
        )
