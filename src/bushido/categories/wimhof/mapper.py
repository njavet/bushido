from .domain import RoundSpec, WimhofSpec, WimhofUnit
from .orm import WimhofRound, WimhofUnitTable


class WimhofMapper:
    @staticmethod
    def to_orm(parsed_unit: WimhofUnit) -> WimhofUnitTable:
        unit = WimhofUnitTable(
            name=parsed_unit.name,
            log_time=parsed_unit.log_time,
            comment=parsed_unit.comment,
        )
        unit.subunits = [
            WimhofRound(round_nr=r.round_nr, breaths=r.breaths, retention=r.retention)
            for r in parsed_unit.data.rounds
        ]
        return unit

    @staticmethod
    def from_orm(orm_unit: WimhofUnitTable) -> WimhofUnit:
        lst = []
        for r in orm_unit.subunits:
            ws = RoundSpec(
                round_nr=r.round_nr, breaths=r.breaths, retention=r.retention
            )
            lst.append(ws)
        pu = WimhofUnit(
            name=orm_unit.name,
            data=WimhofSpec(rounds=lst),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
