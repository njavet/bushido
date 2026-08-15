from typing import override

from bushidolib.wimhof import WimhofRoundData, WimhofData, WimhofUnit

from ..models import WimhofRound, WimhofUnitTable
from ._base import BaseUnitRepo


class WimhofUnitRepo(BaseUnitRepo[WimhofUnit, WimhofUnitTable]):
    orm_cls = WimhofUnitTable

    @override
    def _to_orm(self, unit: WimhofUnit) -> WimhofUnitTable:
        setting_id = self.get_unit_setting_id(unit.name)
        orm_unit = WimhofUnitTable(
            unit_setting_id=setting_id,
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
        name = self.get_unit_setting_name(orm_unit.unit_setting_id)
        lst = []
        for r in orm_unit.subunits:
            ws = WimhofRoundData(
                round_nr=r.round_nr, breaths=r.breaths, retention=r.retention
            )
            lst.append(ws)
        return WimhofUnit(
            name=name,
            data=WimhofData(rounds=lst),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
