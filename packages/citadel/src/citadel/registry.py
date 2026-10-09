import datetime
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from citadel.persistence.repos import (
    BarbellUnitRepo,
    BaseUnitRepo,
    ChronoUnitRepo,
    LiftingUnitRepo,
    LogUnitRepo,
    MartialArtsUnitRepo,
    RunningUnitRepo,
    SkippingUnitRepo,
    SwimmingUnitRepo,
    WimhofUnitRepo,
    WorkUnitRepo,
)
from citadel.unit import LoggedUnit, RawUnit
from citadel.unit.cardio import (
    build_running_unit,
    build_skipping_unit,
    build_swimming_unit,
)
from citadel.unit.log import build_log_unit
from citadel.unit.martial_arts import (
    build_chrono_unit,
    build_martial_arts_unit,
    build_wimhof_unit,
)
from citadel.unit.strength import build_lifting_unit, build_bilateral_unit, build_unilateral_unit
from citadel.unit.work import build_work_unit


@dataclass(frozen=True)
class UnitSpec:
    repo: type[BaseUnitRepo[Any, Any]]
    build_unit: Callable[[RawUnit, datetime.datetime], LoggedUnit]


UNIT_REGISTRY: dict[str, UnitSpec] = {
    "running": UnitSpec(repo=RunningUnitRepo, build_unit=build_running_unit),
    "swimming": UnitSpec(repo=SwimmingUnitRepo, build_unit=build_swimming_unit),
    "skipping": UnitSpec(repo=SkippingUnitRepo, build_unit=build_skipping_unit),
    "log": UnitSpec(repo=LogUnitRepo, build_unit=build_log_unit),
    "chrono": UnitSpec(repo=ChronoUnitRepo, build_unit=build_chrono_unit),
    "karate": UnitSpec(repo=MartialArtsUnitRepo, build_unit=build_martial_arts_unit),
    "grappling": UnitSpec(repo=MartialArtsUnitRepo, build_unit=build_martial_arts_unit),
    "lifting": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "squat": UnitSpec(repo=BarbellUnitRepo, build_unit=build_barbell_unit),
    "deadlift": UnitSpec(repo=BarbellUnitRepo, build_unit=build_barbell_unit),
    "benchpress": UnitSpec(repo=BarbellUnitRepo, build_unit=build_barbell_unit),
    "overheadpress": UnitSpec(repo=BarbellUnitRepo, build_unit=build_barbell_unit),
    "rows": UnitSpec(repo=BarbellUnitRepo, build_unit=build_barbell_unit),
    "curls": UnitSpec(repo=BarbellUnitRepo, build_unit=build_barbell_unit),
    "shoulder": UnitSpec(repo=BarbellUnitRepo, build_unit=build_barbell_unit),
    "neck": UnitSpec(repo=BarbellUnitRepo, build_unit=build_barbell_unit),
    "work": UnitSpec(repo=WorkUnitRepo, build_unit=build_work_unit),
    "wimhof": UnitSpec(repo=WimhofUnitRepo, build_unit=build_wimhof_unit),
}


"""
one level higher grouping:
* cardio screen
    running, swimming, skipping
* strength
    lifting, squat, deadlift, benchpress, overheadpress, rows, curls, shoulder, neck
* martial arts
    karate, grappling, chrono parts
* breathing
    wimhof, chrono parts
* work
    work
* log
    log
"""
