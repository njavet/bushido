import datetime
from dataclasses import Field
from typing import Annotated

from pydantic import BaseModel

from bushidolib.category.cardio import CardioData
from bushidolib.category.gym import GymData
from bushidolib.category.lifting import LiftingData
from bushidolib.category.wimhof import WimhofData
from bushidolib.constants import UnitCategory


class UnitSetting(BaseModel):
    name: str
    category: UnitCategory


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    options: list[str]
    comment: str | None


UnitData = Annotated[
    CardioData | GymData | LiftingData | WimhofData,
    Field(discriminator="unit_category"),
]

class BaseUnit(BaseModel):
    name: str
    log_time: datetime.datetime
    comment: str | None
