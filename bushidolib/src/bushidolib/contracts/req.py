import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from bushidolib.constants import UnitCategory


class LogUnitRequest(BaseModel):
    unit_name: str
    tokens: tuple[str, ...]
    log_time: datetime.datetime
    comment: str | None = None


class BaseLoadUnitRequest(BaseModel):
    unit_category: UnitCategory
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None


class CardioLoadUnitRequest(BaseLoadUnitRequest):
    unit_category: Literal[UnitCategory.CARDIO] = UnitCategory.CARDIO


class GymLoadUnitRequest(BaseLoadUnitRequest):
    unit_category: Literal[UnitCategory.GYM] = UnitCategory.GYM


class LiftingLoadUnitRequest(BaseLoadUnitRequest):
    unit_category: Literal[UnitCategory.LIFTING] = UnitCategory.LIFTING


class WimhofLoadUnitRequest(BaseLoadUnitRequest):
    unit_category: Literal[UnitCategory.WIMHOF] = UnitCategory.WIMHOF


LoadUnitRequest = Annotated[
    LiftingLoadUnitRequest
    | CardioLoadUnitRequest
    | GymLoadUnitRequest
    | WimhofLoadUnitRequest,
    Field(discriminator="unit_category"),
]
