import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class BaseLoadUnitRequest(BaseModel):
    unit_type: str
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None


class CardioLoadUnitRequest(BaseLoadUnitRequest):
    unit_type: Literal["cardio"] = "cardio"


class GymLoadUnitRequest(BaseLoadUnitRequest):
    unit_type: Literal["gym"] = "gym"


class LiftingLoadUnitRequest(BaseLoadUnitRequest):
    unit_type: Literal["lifting"] = "lifting"


class WimhofLoadUnitRequest(BaseLoadUnitRequest):
    unit_type: Literal["wimhof"] = "wimhof"


LoadUnitRequest = Annotated[
    LiftingLoadUnitRequest
    | CardioLoadUnitRequest
    | GymLoadUnitRequest
    | WimhofLoadUnitRequest,
    Field(discriminator="unit_type"),
]
