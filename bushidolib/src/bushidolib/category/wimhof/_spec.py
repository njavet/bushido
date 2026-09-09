from typing import Literal

from pydantic import BaseModel

from bushidolib.constants import UnitCategory
from bushidolib.unit import BaseUnit

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
