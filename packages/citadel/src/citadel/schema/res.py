import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from citadel.unit.cardio import RunningUnit, SkippingUnit, SwimmingUnit
from citadel.unit.log import LogUnit
from citadel.unit.martial_arts import ChronoUnit, MartialArtsUnit, WimhofUnit
from citadel.unit.strength import BilateralUnit, LiftingUnit, UnilateralUnit
from citadel.unit.work import WorkUnit


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
    | WorkUnit
    | LiftingUnit
    | SwimmingUnit
    | RunningUnit
    | SkippingUnit
    | ChronoUnit
    | LogUnit
    | MartialArtsUnit,
    Field(discriminator="unit_type"),
]
