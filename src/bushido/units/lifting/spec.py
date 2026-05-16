from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SetData:
    set_nr: int
    weight: float
    reps: float
    rest: float


@dataclass(frozen=True, slots=True)
class Data:
    variant: str | None
    program: str | None
    sets: list[SetData]


grammar = """
<name> (<weight> <reps> [<rest>])+ -p <program> -v <variant> # [<comment>]
"""
