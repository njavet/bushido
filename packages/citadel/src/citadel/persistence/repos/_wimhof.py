from typing import override

from citadel.domain.unit import RoundData, WimhofUnit

from ...domain.unit import UnitType
from ..models import UnitTable, WimhofRound, WimhofUnitTable
from ._base import BaseUnitRepo


class WimhofUnitRepo(BaseUnitRepo[WimhofUnit]):
    unit_type = UnitType.wimhof

    @override
    def add_unit(self, unit: WimhofUnit, spartan_id: int) -> None:
        orm_unit = UnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            wimhof=WimhofUnitTable(
                zen_mode=unit.zen_mode,
                guide=unit.guide,
                subunits=[
                    WimhofRound(
                        round_nr=r.round_nr, breaths=r.breaths, retention=r.retention
                    )
                    for r in unit.rounds
                ],
            ),
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: UnitTable) -> WimhofUnit:
        assert orm_unit.wimhof is not None
        rounds = [
            RoundData(round_nr=r.round_nr, breaths=r.breaths, retention=r.retention)
            for r in orm_unit.wimhof.subunits
        ]

        return WimhofUnit(
            name=orm_unit.name,
            rounds=rounds,
            zen_mode=orm_unit.wimhof.zen_mode,
            guide=orm_unit.wimhof.guide,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
