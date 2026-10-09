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
from citadel.schema.res import LoggedUnit
from citadel.unit import RawUnit
from citadel.unit.cardio import (
    build_running_unit,
    build_skipping_unit,
    build_swimming_unit,
)
from citadel.unit.log import build_log_unit
from citadel.unit.martial_arts import (
    build_chrono_unit,
    build_grappling_unit,
    build_karate_unit,
    build_wimhof_unit,
)
from citadel.unit.strength import (
    build_benchpress_unit,
    build_curls_unit,
    build_deadlift_unit,
    build_lifting_unit,
    build_neck_unit,
    build_ohp_unit,
    build_rows_unit,
    build_shoulder_unit,
    build_squat_unit,
)
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
    "karate": UnitSpec(repo=MartialArtsUnitRepo, build_unit=build_karate_unit),
    "grappling": UnitSpec(repo=MartialArtsUnitRepo, build_unit=build_grappling_unit),
    "lifting": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "squat": UnitSpec(repo=BarbellUnitRepo, build_unit=build_squat_unit),
    "deadlift": UnitSpec(repo=BarbellUnitRepo, build_unit=build_deadlift_unit),
    "benchpress": UnitSpec(repo=BarbellUnitRepo, build_unit=build_benchpress_unit),
    "overheadpress": UnitSpec(repo=BarbellUnitRepo, build_unit=build_ohp_unit),
    "rows": UnitSpec(repo=BarbellUnitRepo, build_unit=build_rows_unit),
    "curls": UnitSpec(repo=BarbellUnitRepo, build_unit=build_curls_unit),
    "shoulder": UnitSpec(repo=BarbellUnitRepo, build_unit=build_shoulder_unit),
    "neck": UnitSpec(repo=BarbellUnitRepo, build_unit=build_neck_unit),
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
