from dataclasses import dataclass

from bushido.dtypes import ParsedUnit


@dataclass(frozen=True, slots=True)
class SetSpec:
    set_nr: int
    weight: float
    reps: float
    rest: float


@dataclass(frozen=True, slots=True)
class LiftingSpec:
    sets: list[SetSpec]


@dataclass(frozen=True, slots=True)
class LiftingUnit(ParsedUnit[LiftingSpec]):
    pass
