from citadel.domain.unit.cali import CaliUnit
from citadel.domain.unit.cardio import RopeSkipUnit, RunningUnit, SwimmingUnit
from citadel.domain.unit.chrono import ChronoUnit
from citadel.domain.unit.log import LogUnit
from citadel.domain.unit.martial_arts import MartialArtsUnit
from citadel.domain.unit.strength import LiftingUnit, StrengthUnit
from citadel.domain.unit.wimhof import WimhofUnit
from citadel.domain.unit.work import WorkUnit

LoggedUnit = (
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
    | MartialArtsUnit
)
