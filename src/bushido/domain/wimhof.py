from dataclasses import dataclass
from enum import StrEnum


class WimhofUnitName(StrEnum):
    wimhof = "wimhof"


@dataclass
class RoundSpec:
    round_nr: int
    breaths: int
    retention: int


@dataclass
class WimhofSpec:
    rounds: list[RoundSpec]
