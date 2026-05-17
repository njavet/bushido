import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from bushido.units import Unit
from bushido.units.wimhof import RoundData, WimhofData

from ..models import WimhofRound, WimhofUnitTable


class WimhofUnitRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_unit(self, unit: Unit[WimhofData]) -> None:
        self.session.add(self._to_orm(unit))
        self.session.commit()

    def fetch_units(
        self,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[WimhofData]]:
        stmt = select(WimhofUnitTable).options(selectinload(WimhofUnitTable.subunits))
        if start_t is not None:
            stmt = stmt.where(start_t <= WimhofUnitTable.log_time)
        if end_t is not None:
            stmt = stmt.where(WimhofUnitTable.log_time <= end_t)
        stmt = stmt.order_by(WimhofUnitTable.log_time.desc())
        return [self._from_orm(unit) for unit in self.session.scalars(stmt)]

    @staticmethod
    def _to_orm(unit: Unit[WimhofData]) -> WimhofUnitTable:
        orm_unit = WimhofUnitTable(
            name=unit.name,
            emoji=unit.emoji,
            log_time=unit.log_time,
            comment=unit.comment,
        )
        orm_unit.subunits = [
            WimhofRound(round_nr=r.round_nr, breaths=r.breaths, retention=r.retention)
            for r in unit.data.rounds
        ]
        return orm_unit

    @staticmethod
    def _from_orm(orm_unit: WimhofUnitTable) -> Unit[WimhofData]:
        lst = []
        for r in orm_unit.subunits:
            ws = RoundData(
                round_nr=r.round_nr, breaths=r.breaths, retention=r.retention
            )
            lst.append(ws)
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=WimhofData(rounds=lst),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
