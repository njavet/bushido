from typing import Annotated

from pydantic import Field

from .cardio import SwimmingUnit, RunningUnit, SkippingUnit
from .log import LogUnit
from .martial_arts import WimhofUnit, MartialArtsUnit, ChronoUnit
from .work import WorkUnit
from .strength import BarbellUnit, LiftingUnit


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
