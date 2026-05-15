from dataclasses import dataclass

from bushido.category.dtypes import ParsedUnit


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
