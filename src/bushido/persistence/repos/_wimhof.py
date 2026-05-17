from bushido.domain.units import Unit
from bushido.domain.units.wimhof import RoundData, WimhofData

from ..models import WimhofRound, WimhofUnitTable
from ._base import BaseUnitRepo


class WimhofUnitRepo(BaseUnitRepo[WimhofData, WimhofUnitTable]):
    orm_cls = WimhofUnitTable

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
