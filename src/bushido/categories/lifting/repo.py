import datetime

from sqlalchemy.orm import Session, selectinload

from bushido.core.repo import UnitRepo

from .orm import LiftingUnitTable


class LiftingRepo(UnitRepo[LiftingUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, LiftingUnitTable)

    def fetch_units(
        self,
        unit_name: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[LiftingUnitTable]:
        return self._fetch_units(
            unit_name=unit_name,
            start_t=start_t,
            end_t=end_t,
            options=[selectinload(LiftingUnitTable.subunits)],
        )
