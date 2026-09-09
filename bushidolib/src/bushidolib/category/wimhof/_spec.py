from typing import Literal

from pydantic import BaseModel

from bushidolib.category.unit import BaseUnit
from bushidolib.constants import UnitCategory

grammar = "<name> (<breaths> <retentions>)+ # [<comment>]"


class WimhofRoundData(BaseModel):
    round_nr: int
    breaths: int
    retention: int


class WimhofData(BaseModel):
    rounds: list[WimhofRoundData]


class WimhofUnit(BaseUnit):
    unit_category: Literal[UnitCategory.WIMHOF] = UnitCategory.WIMHOF
    data: WimhofData
