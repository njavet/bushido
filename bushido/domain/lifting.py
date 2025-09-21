from typing import Optional
from dataclasses import dataclass

# project imports


@dataclass
class SetSpec:
    weight: float
    reps: float
    rest: float


@dataclass
class Exercise:
    sets: list[SetSpec]
