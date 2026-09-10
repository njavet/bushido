from pydantic import BaseModel

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
    sets: list[LiftingSetData]
