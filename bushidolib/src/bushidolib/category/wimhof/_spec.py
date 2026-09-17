from pydantic import BaseModel

from bushidolib.schema.unit import BaseUnit


class WimhofRoundData(BaseModel):
    round_nr: int
    breaths: int
    retention: int


class WimhofData(BaseModel):
    rounds: list[WimhofRoundData]


class WimhofUnit(BaseUnit):
    rounds: list[WimhofRoundData]
