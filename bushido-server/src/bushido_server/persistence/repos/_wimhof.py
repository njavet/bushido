from typing import override

from bushidolib.category.wimhof import WimhofData, WimhofRoundData, WimhofUnit

from ..models import WimhofRound, WimhofUnitTable
from ._base import BaseUnitRepo


class WimhofUnitRepo(BaseUnitRepo[WimhofUnit, WimhofUnitTable]):
    orm_cls = WimhofUnitTable

    @override
    def _to_orm(self, unit: WimhofUnit) -> WimhofUnitTable:
        orm_unit = WimhofUnitTable(
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
        )
        orm_unit.subunits = [
            WimhofRound(round_nr=r.round_nr, breaths=r.breaths, retention=r.retention)
            for r in unit.data.rounds
        ]
        return orm_unit

    @override
    def _from_orm(self, orm_unit: WimhofUnitTable) -> WimhofUnit:
        lst = []
        for r in orm_unit.subunits:
            ws = WimhofRoundData(
                round_nr=r.round_nr, breaths=r.breaths, retention=r.retention
            )
            lst.append(ws)
        return WimhofUnit(
            name=orm_unit.name,
            data=WimhofData(rounds=lst),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
