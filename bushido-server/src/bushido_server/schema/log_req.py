from typing import Literal, Annotated

from pydantic import BaseModel, Field


class BaseLogRequest(BaseModel):
    user_name: str
    unit_type: str
    unit_name: str
    tokens: tuple[str, ...]
    comment: str | None = None


class LiftingLogRequest(BaseLogRequest):
    unit_type: Literal["lifting"]


class CardioLogRequest(BaseLogRequest):
    unit_type: Literal["cardio"]


class GymLogRequest(BaseLogRequest):
    unit_type: Literal["gym"]


class WimhofLogRequest(BaseLogRequest):
    unit_type: Literal["wimhof"]


UnitLogRequest = Annotated[
    LiftingLogRequest | CardioLogRequest | GymLogRequest | WimhofLogRequest,
    Field(discriminator="unit_type"),
]
