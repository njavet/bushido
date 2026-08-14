import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from bushidolib.constants import UnitCategory


class BaseLogUnitRequest(BaseModel):
    unit_category: UnitCategory
    unit_name: str
    tokens: tuple[str, ...]
    log_time: datetime.datetime
    comment: str | None = None


class CardioLogUnitRequest(BaseLogUnitRequest):
    unit_category: Literal[UnitCategory.CARDIO] = UnitCategory.CARDIO


class GymLogUnitRequest(BaseLogUnitRequest):
    unit_category: Literal[UnitCategory.GYM] = UnitCategory.GYM


class LiftingLogUnitRequest(BaseLogUnitRequest):
    unit_category: Literal[UnitCategory.LIFTING] = UnitCategory.LIFTING


class WimhofLogUnitRequest(BaseLogUnitRequest):
    unit_category: Literal[UnitCategory.WIMHOF] = UnitCategory.WIMHOF


LogUnitRequest = Annotated[
    LiftingLogUnitRequest
    | CardioLogUnitRequest
    | GymLogUnitRequest
    | WimhofLogUnitRequest,
    Field(discriminator="unit_category"),
]
