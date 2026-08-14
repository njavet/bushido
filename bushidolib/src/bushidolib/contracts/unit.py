import datetime
from enum import StrEnum

from pydantic import BaseModel


class UnitCategory(StrEnum):
    CARDIO = "cardio"
    GYM = "gym"
    LIFTING = "lifting"
    WIMHOF = "wimhof"


class UnitSetting(BaseModel):
    name: str
    category: UnitCategory


class BaseUnit(BaseModel):
    name: str
    log_time: datetime.datetime
    comment: str | None


class CardioData(BaseModel):
    start_t: datetime.time
    seconds: float
    location: str
    distance: float | None
    avg_hr: int | None
    max_hr: int | None
    calories: int | None


class CardioUnit(BaseUnit):
    data: CardioData


class GymData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = None
    focus: str | None = None


class GymUnit(BaseUnit):
    data: GymData


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
