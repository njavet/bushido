from bushido.units.base import Unit

from .db_model import WimhofRound, WimhofUnitTable
from .unit import RoundData, WimhofData


class WimhofMapper:
    @staticmethod
    def to_orm(unit: Unit[WimhofData]) -> WimhofUnitTable:
        unit = WimhofUnitTable(
            name=unit.name,
            emoji=unit.emoji,
            log_time=unit.log_time,
            comment=unit.comment,
        )
        unit.rounds = [
            WimhofRound(round_nr=r.round_nr, breaths=r.breaths, retention=r.retention)
            for r in unit.data.rounds
        ]
        return unit

    @staticmethod
    def from_orm(orm_unit: WimhofUnitTable) -> Unit[WimhofData]:
        lst = []
        for r in orm_unit.rounds:
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
