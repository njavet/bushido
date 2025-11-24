from bushido.modules.dtypes import ParsedUnit, UnitMapper

from .domain import RoundSpec, WimhofSpec
from .orm import WimhofRound, WimhofUnit


class WimhofMapper(UnitMapper[WimhofSpec, WimhofUnit, WimhofRound]):
    @staticmethod
    def to_orm(
        parsed_unit: ParsedUnit[WimhofSpec],
    ) -> tuple[WimhofUnit, list[WimhofRound]]:
        unit = WimhofUnit(name=parsed_unit.name, comment=parsed_unit.comment)
        lst = []
        for i, s in enumerate(parsed_unit.data.rounds):
            wr = WimhofRound(round_nr=i, breaths=s.breaths, retention=s.retention)
            lst.append(wr)
        return unit, lst

    @staticmethod
    def from_orm(
        orms: tuple[WimhofUnit, list[WimhofRound]],
    ) -> ParsedUnit[WimhofSpec]:
        unit, rounds = orms
        lst = []
        for i, s in enumerate(rounds):
            ws = RoundSpec(round_nr=i, breaths=s.breaths, retention=s.retention)
            lst.append(ws)
        pu = ParsedUnit(
            name=unit.name,
            data=WimhofSpec(rounds=lst),
            comment=unit.comment,
        )
        return pu
