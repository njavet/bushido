import datetime
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from bushidolib.unit.base import BaseUnit, RawUnit
from bushidolib.unit.cali import build_cali_unit
from bushidolib.unit.cardio import build_cardio_unit
from bushidolib.unit.chrono import build_chrono_unit
from bushidolib.unit.log import build_log_unit
from bushidolib.unit.martial_arts import build_martial_arts_unit
from bushidolib.unit.strength import (
    build_lifting_unit,
    build_strength_unit,
)
from bushidolib.unit.wimhof import build_wimhof_unit
from bushidolib.unit.work import build_work_unit

from citadel.persistence.repos import (
    BaseUnitRepo,
    CaliUnitRepo,
    ChronoUnitRepo,
    LiftingUnitRepo,
    LogUnitRepo,
    MartialArtsUnitRepo,
    RopeSkipUnitRepo,
    RunningUnitRepo,
    StrengthUnitRepo,
    SwimmingUnitRepo,
    WimhofUnitRepo,
    WorkUnitRepo,
)


@dataclass(frozen=True)
class UnitSpec:
    repo: type[BaseUnitRepo[Any, Any]]
    build_unit: Callable[[RawUnit, datetime.datetime], BaseUnit]


UNIT_REGISTRY: dict[str, UnitSpec] = {
    "cali": UnitSpec(repo=CaliUnitRepo, build_unit=build_cali_unit),
    "running": UnitSpec(repo=RunningUnitRepo, build_unit=build_cardio_unit),
    "swimming": UnitSpec(repo=SwimmingUnitRepo, build_unit=build_cardio_unit),
    "skipping": UnitSpec(repo=RopeSkipUnitRepo, build_unit=build_cardio_unit),
    "log": UnitSpec(repo=LogUnitRepo, build_unit=build_log_unit),
    "chrono": UnitSpec(repo=ChronoUnitRepo, build_unit=build_chrono_unit),
    "karate": UnitSpec(repo=MartialArtsUnitRepo, build_unit=build_martial_arts_unit),
    "grappling": UnitSpec(repo=MartialArtsUnitRepo, build_unit=build_martial_arts_unit),
    "strength": UnitSpec(repo=StrengthUnitRepo, build_unit=build_strength_unit),
    "squat": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "deadlift": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "benchpress": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "overheadpress": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "rows": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "curls": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "shoulder": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "neck": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "work": UnitSpec(repo=WorkUnitRepo, build_unit=build_work_unit),
    "wimhof": UnitSpec(repo=WimhofUnitRepo, build_unit=build_wimhof_unit),
}
