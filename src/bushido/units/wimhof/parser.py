from dataclasses import dataclass
from enum import StrEnum

from bushido.core.result import Err, Ok, Result
from bushido.units.parsing.base import UnitParser


class WimhofUnitName(StrEnum):
    wimhof = "wimhof"


@dataclass(frozen=True, slots=True)
class RoundSpec:
    round_nr: int
    breaths: int
    retention: int


@dataclass(frozen=True, slots=True)
class WimhofSpec:
    rounds: list[RoundSpec]


@dataclass(frozen=True, slots=True)
class WimhofParser(UnitParser[WimhofSpec]):
    grammar = ""
    unit_names = [unit_name for unit_name in WimhofUnitName]

    @staticmethod
    def parse(tokens: tuple[str, ...]) -> Result[WimhofSpec]:
        breaths = [int(b) for b in tokens[::2]]
        retentions = [int(r) for r in tokens[1::2]]
        if len(breaths) == 0:
            return Err("at least one round")
        if len(breaths) != len(retentions):
            return Err("breaths and retentions don't match")
        if any(x < 0 for x in breaths):
            return Err("breaths must all be positive")
        if any(x < 0 for x in retentions):
            return Err("Retentions must all be positive")

        ex = WimhofSpec(
            rounds=[
                RoundSpec(round_nr=i, breaths=b, retention=r)
                for i, (b, r) in enumerate(zip(breaths, retentions))
            ]
        )
        return Ok(ex)
