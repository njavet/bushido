from dataclasses import dataclass

from pydantic import BaseModel

from bushidolib.unit import BaseUnit

grammar = "<name> (<breaths> <retentions>)+ # [<comment>]"
class WimhofRoundData(BaseModel):
    round_nr: int
    breaths: int
    retention: int


class WimhofData(BaseModel):
    rounds: list[WimhofRoundData]


class WimhofUnit(BaseUnit):
    data: WimhofData

