import datetime
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from citadel.domain.dtypes import LoggedUnit
from citadel.domain.unit import (
    RawUnit,
    build_barbell_unit,
    build_chrono_unit,
    build_lifting_unit,
    build_log_unit,
    build_martial_arts_unit,
    build_running_unit,
    build_skipping_unit,
    build_swimming_unit,
    build_wimhof_unit,
    build_work_unit,
)
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
