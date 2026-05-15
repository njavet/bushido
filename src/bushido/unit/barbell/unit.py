from dataclasses import dataclass

from ..base import Unit


@dataclass(frozen=True, slots=True)
class SetData:
    set_nr: int
    weight: float
    reps: float
    rest: float


@dataclass(frozen=True, slots=True)
class BarbellData:
    variant: str | None
    program: str | None
    sets: list[SetData]


@dataclass(frozen=True, slots=True)
class BarbellUnit(Unit):
    variant: str | None
    program: str | None
    sets: list[SetData]
