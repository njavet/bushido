from typing import Annotated

from pydantic import Field

from citadel.domain.cali.cali import CaliUnit
from citadel.domain.cardio.cardio import RopeSkipUnit, RunningUnit, SwimmingUnit
from citadel.domain.chrono.chrono import ChronoUnit
from citadel.domain.log.log import LogUnit
from citadel.domain.martial_arts.martial_arts import MartialArtsUnit
from citadel.domain.strength.strength import LiftingUnit, StrengthUnit
from citadel.domain.wimhof.wimhof import WimhofUnit
from citadel.domain.work.work import WorkUnit

type LoggedUnit = Annotated[
    CaliUnit
    | WimhofUnit
    | WorkUnit
    | StrengthUnit
    | LiftingUnit
    | SwimmingUnit
    | RunningUnit
    | RopeSkipUnit
    | ChronoUnit
    | LogUnit
    | MartialArtsUnit,
    Field(discriminator="unit_type"),
]
