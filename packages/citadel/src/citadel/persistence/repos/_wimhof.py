from typing import override

from sqlalchemy.orm import selectinload

from citadel.unit import UnitType
from citadel.unit.martial_arts import RoundData, WimhofUnit

from ..models import WimhofRound, WimhofUnitTable
from ._base import BaseUnitRepo


class WimhofUnitRepo(BaseUnitRepo[WimhofUnit, WimhofUnitTable]):
    orm_cls = WimhofUnitTable
    unit_type = UnitType.wimhof
    load_options = (selectinload(WimhofUnitTable.subunits),)

    @override
    def add_unit(self, unit: WimhofUnit, spartan_id: int) -> None:
        orm_unit = WimhofUnitTable(
            spartan_id=spartan_id,
            unit_type=self.unit_type,
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            zen_mode=unit.zen_mode,
            guide=unit.guide,
            subunits=[
                WimhofRound(
                    round_nr=r.round_nr, breaths=r.breaths, retention=r.retention
                )
                for r in unit.rounds
            ],
        )
        self.session.add(orm_unit)

    @override
    def _from_orm(self, orm_unit: WimhofUnitTable) -> WimhofUnit:
        rounds = [
            RoundData(round_nr=r.round_nr, breaths=r.breaths, retention=r.retention)
            for r in orm_unit.subunits
        ]

        return WimhofUnit(
            name=orm_unit.name,
            rounds=rounds,
            zen_mode=orm_unit.zen_mode,
            guide=orm_unit.guide,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
