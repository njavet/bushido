import datetime

from sqlalchemy.orm import Session, selectinload

from bushido.units.repo import UnitRepo

from .db_model import WimhofUnitTable


class WimhofRepo(UnitRepo[WimhofUnitTable]):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session, WimhofUnitTable)

    def fetch_units(
        self,
        unit_name: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[WimhofUnitTable]:
        return self._fetch_units(
            unit_name=unit_name,
            start_t=start_t,
            end_t=end_t,
            options=[selectinload(WimhofUnitTable.subunits)],
        )
