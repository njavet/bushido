from pydantic import BaseModel


class WimhofRoundData(BaseModel):
    round_nr: int
    breaths: int
    retention: int


class WimhofData(BaseModel):
    rounds: list[WimhofRoundData]
