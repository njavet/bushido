from typing import Annotated

from pydantic import Field

from .cardio import RunningUnit, SkippingUnit, SwimmingUnit
from .log import LogUnit
from .martial_arts import ChronoUnit, MartialArtsUnit, WimhofUnit
from .strength import BilateralUnit, LiftingUnit, UnilateralUnit
from .work import WorkUnit

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
