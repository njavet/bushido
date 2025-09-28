from dataclasses import dataclass


@dataclass
class SetSpec:
    set_nr: int
    weight: float
    reps: float
    rest: float


@dataclass
class ExerciseSpec:
    sets: list[SetSpec]
