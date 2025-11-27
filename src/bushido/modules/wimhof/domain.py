from dataclasses import dataclass
from enum import StrEnum

from bushido.core.dtypes import UnitData

from .orm import WimhofUnit


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


def format_wimhof_unit(unit: WimhofUnit) -> str:
    return unit.name
