from typing import Literal

from pydantic import BaseModel

from bushidolib.category.unit import BaseUnit
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
    variant: str | None
    program: str | None
    sets: list[LiftingSetData]


class LiftingUnit(BaseUnit):
    unit_category: Literal[UnitCategory.LIFTING] = UnitCategory.LIFTING
    data: LiftingData
