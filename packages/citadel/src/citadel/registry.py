import datetime
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from citadel.bcl.parsers.log import LogUnitCommand
from citadel.persistence.repos import (
    BarbellUnitRepo,
    BaseUnitRepo,
    ChronoUnitRepo,
    LiftingUnitRepo,
    MartialArtsUnitRepo,
    RunningUnitRepo,
    WimhofUnitRepo,
)
from citadel.schema.res import LoggedUnit
from citadel.unit.cardio import (
    build_running_unit,
)
from citadel.unit.martial_arts import (
    build_chrono_unit,
    build_grappling_unit,
    build_karate_unit,
    build_wimhof_unit,
)
from citadel.unit.strength import (
    build_benchpress_unit,
    build_deadlift_unit,
    build_lifting_unit,
    build_rows_unit,
    build_squat_unit,
)

ölm = 2


@dataclass(frozen=True)
class UnitSpec:
    repo: type[BaseUnitRepo[Any, Any]]
    build_unit: Callable[[LogUnitCommand, datetime.datetime], LoggedUnit]


UNIT_REGISTRY: dict[str, UnitSpec] = {
    "running": UnitSpec(repo=RunningUnitRepo, build_unit=build_running_unit),
    "split_machine": UnitSpec(repo=ChronoUnitRepo, build_unit=build_chrono_unit),
    "karate": UnitSpec(repo=MartialArtsUnitRepo, build_unit=build_karate_unit),
    "grappling": UnitSpec(repo=MartialArtsUnitRepo, build_unit=build_grappling_unit),
    "lifting": UnitSpec(repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    "squat": UnitSpec(repo=BarbellUnitRepo, build_unit=build_squat_unit),
    "deadlift": UnitSpec(repo=BarbellUnitRepo, build_unit=build_deadlift_unit),
    "benchpress": UnitSpec(repo=BarbellUnitRepo, build_unit=build_benchpress_unit),
    "rows": UnitSpec(repo=BarbellUnitRepo, build_unit=build_rows_unit),
    "wimhof": UnitSpec(repo=WimhofUnitRepo, build_unit=build_wimhof_unit),
}
