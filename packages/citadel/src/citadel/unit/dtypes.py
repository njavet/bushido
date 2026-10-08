from typing import Annotated

from pydantic import Field

from citadel.unit import (
    BarbellUnit,
    ChronoUnit,
    LiftingUnit,
    LogUnit,
    MartialArtsUnit,
    RopeSkipUnit,
    RunningUnit,
    SwimmingUnit,
    WimhofUnit,
    WorkUnit,
)

type LoggedUnit = Annotated[
    WimhofUnit
    | BarbellUnit
    | WorkUnit
    | LiftingUnit
    | SwimmingUnit
    | RunningUnit
    | RopeSkipUnit
    | ChronoUnit
    | LogUnit
    | MartialArtsUnit,
    Field(discriminator="unit_type"),
]
