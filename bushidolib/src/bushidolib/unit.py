from dataclasses import dataclass
from typing import Annotated

from bushidolib.category.cardio import CardioData
from bushidolib.category.gym import GymData
from bushidolib.category.lifting import LiftingData
from bushidolib.category.wimhof import WimhofData


@dataclass(frozen=True, slots=True)
class RawUnit:
    name: str
    tokens: tuple[str, ...]
    options: list[str]
    comment: str | None = None


UnitData = Annotated[
    CardioData | GymData | LiftingData | WimhofData,
]

@dataclass(frozen=True, slots=True)
class Unit:
    comment: str | None
    data: UnitData
