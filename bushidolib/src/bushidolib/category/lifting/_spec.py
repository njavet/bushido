from typing import Literal

from pydantic import BaseModel

from bushidolib.constants import UnitCategory

grammar = """
<name> (<weight> <reps> [<rest>])+ -p <program> -v <variant> # [<comment>]
"""


class LiftingSetData(BaseModel):
    set_nr: int
    weight: float
    reps: float
    rest: float


class LiftingData(BaseModel):
    unit_category: Literal[UnitCategory.LIFTING] = UnitCategory.LIFTING
    variant: str | None
    sets: list[LiftingSetData]
