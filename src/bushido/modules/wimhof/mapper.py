from bushido.core.dtypes import ParsedUnit
from bushido.modules.mapper import UnitMapper

from .domain import RoundSpec, WimhofSpec
from .orm import WimhofRound, WimhofUnit


class WimhofMapper(UnitMapper[WimhofSpec, WimhofUnit, WimhofRound]):
    @staticmethod
    def to_orm(
        parsed_unit: ParsedUnit[WimhofSpec],
    ) -> tuple[WimhofUnit, list[WimhofRound]]:
        unit = WimhofUnit(
            name=parsed_unit.name,
            log_time=parsed_unit.log_time,
            comment=parsed_unit.comment,
        )
        lst = []
        for r in parsed_unit.data.rounds:
            wr = WimhofRound(
                round_nr=r.round_nr, breaths=r.breaths, retention=r.retention
            )
            lst.append(wr)
        return unit, lst

    @staticmethod
    def from_orm(
        orms: tuple[WimhofUnit, list[WimhofRound]],
    ) -> ParsedUnit[WimhofSpec]:
        unit, rounds = orms
        lst = []
        for r in rounds:
            ws = RoundSpec(
                round_nr=r.round_nr, breaths=r.breaths, retention=r.retention
            )
            lst.append(ws)
        pu = ParsedUnit(
            name=unit.name,
            data=WimhofSpec(rounds=lst),
            log_time=unit.log_time,
            comment=unit.comment,
        )
        return pu
