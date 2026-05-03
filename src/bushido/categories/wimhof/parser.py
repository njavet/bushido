from dataclasses import dataclass
from enum import StrEnum

from ..exceptions import ParsingError
from ..parsing.base import UnitParser


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
    unit_names = [unit_name.value for unit_name in WimhofUnitName]

    @staticmethod
    def parse(tokens: tuple[str, ...]) -> WimhofSpec:
        breaths = [int(b) for b in tokens[::2]]
        retentions = [int(r) for r in tokens[1::2]]
        if len(breaths) == 0:
            raise ParsingError("at least one round")
        if len(breaths) != len(retentions):
            raise ParsingError("breaths and retentions don't match")
        if any(x < 0 for x in breaths):
            raise ParsingError("breaths must all be positive")
        if any(x < 0 for x in retentions):
            raise ParsingError("retentions must all be positive")

        return WimhofSpec(
            rounds=[
                RoundSpec(round_nr=i, breaths=b, retention=r)
                for i, (b, r) in enumerate(zip(breaths, retentions))
            ]
        )
