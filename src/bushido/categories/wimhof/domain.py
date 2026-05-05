from dataclasses import dataclass
from enum import StrEnum

from ..dtypes import ParsedUnit


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
class WimhofUnit(ParsedUnit[WimhofSpec]):
    pass
