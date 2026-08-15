from pydantic import BaseModel

from bushidolib.unit import BaseUnit

grammar = """
<name> (<weight> <reps> [<rest>])+ -p <program> -v <variant> # [<comment>]
"""


class LiftingSetData(BaseModel):
    set_nr: int
    weight: float
    reps: float
    rest: float


class LiftingData(BaseModel):
    variant: str | None
    program: str | None
    sets: list[LiftingSetData]


class LiftingUnit(BaseUnit):
    data: LiftingData
