from dataclasses import dataclass


@dataclass
class SetSpec:
    weight: float
    reps: float
    rest: float


@dataclass
class ExerciseSpec:
    sets: list[SetSpec]
