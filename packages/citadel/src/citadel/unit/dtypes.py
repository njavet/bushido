from typing import Annotated

from pydantic import Field

from .cardio import RunningUnit, SkippingUnit, SwimmingUnit
from .log import LogUnit
from .martial_arts import ChronoUnit, MartialArtsUnit, WimhofUnit
from .strength import BarbellUnit, LiftingUnit
from .work import WorkUnit

type LoggedUnit = Annotated[
    WimhofUnit
    | BarbellUnit
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
