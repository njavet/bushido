from typing import Optional
from dataclasses import dataclass


@dataclass
class SetSpec:
    weight: float
    reps: float
    rest: Optional[float]


@dataclass
class Exercise:
    name: str
    sets: list[SetSpec]

