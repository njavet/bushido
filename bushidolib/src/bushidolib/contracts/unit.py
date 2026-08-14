import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


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


class CardioUnit(BaseUnit):
    data: dict[str, float] = Field(default_factory=dict)
