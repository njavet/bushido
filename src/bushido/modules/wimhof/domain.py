from dataclasses import dataclass
from enum import StrEnum

from bushido.modules.domain import UnitData


class WimhofUnitName(StrEnum):
    wimhof = "wimhof"


@dataclass(frozen=True, slots=True)
class RoundSpec:
    round_nr: int
    breaths: int
    retention: int


@dataclass(frozen=True, slots=True)
class WimhofSpec(UnitData):
    rounds: list[RoundSpec]
