from typing import Literal

from pydantic import BaseModel

from bushidolib.constants import UnitCategory


class WimhofRoundData(BaseModel):
    round_nr: int
    breaths: int
    retention: int


class WimhofData(BaseModel):
    rounds: list[WimhofRoundData]
