import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class BaseLogUnitRequest(BaseModel):
    user_name: str
    unit_type: str
    unit_name: str
    tokens: tuple[str, ...]
    log_time: datetime.datetime
    comment: str | None = None


class CardioLogUnitRequest(BaseLogUnitRequest):
    unit_type: Literal["cardio"]


class GymLogUnitRequest(BaseLogUnitRequest):
    unit_type: Literal["gym"]


class LiftingLogUnitRequest(BaseLogUnitRequest):
    unit_type: Literal["lifting"]


class WimhofLogUnitRequest(BaseLogUnitRequest):
    unit_type: Literal["wimhof"]


LogUnitRequest = Annotated[
    LiftingLogUnitRequest
    | CardioLogUnitRequest
    | GymLogUnitRequest
    | WimhofLogUnitRequest,
    Field(discriminator="unit_type"),
]
