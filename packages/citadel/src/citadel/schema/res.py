import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from citadel.unit.cardio import RunningUnit
from citadel.unit.martial_arts import ChronoUnit, MartialArtsUnit, WimhofUnit
from citadel.unit.strength import BilateralUnit, LiftingUnit, UnilateralUnit


class SpartanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime.datetime


type LoggedUnit = Annotated[
    WimhofUnit
    | BilateralUnit
    | UnilateralUnit
    | LiftingUnit
    | RunningUnit
    | ChronoUnit
    | MartialArtsUnit,
    Field(discriminator="unit_type"),
]


class UnitsPerDay(BaseModel):
    day: datetime.date
    units: list[LoggedUnit]
