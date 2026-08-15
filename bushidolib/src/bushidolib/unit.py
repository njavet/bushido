import datetime

from pydantic import BaseModel

from bushidolib.constants import UnitCategory


class UnitSetting(BaseModel):
    name: str
    category: UnitCategory


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    comment: str | None


class BaseUnit(BaseModel):
    name: str
    log_time: datetime.datetime
    comment: str | None




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


class WimhofRoundData(BaseModel):
    round_nr: int
    breaths: int
    retention: int


class WimhofData(BaseModel):
    rounds: list[WimhofRoundData]


class WimhofUnit(BaseUnit):
    data: WimhofData


LoadedUnits = list[CardioUnit] | list[GymUnit] | list[LiftingUnit] | list[WimhofUnit]
