import datetime
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from bushido_server.persistence.repos import (
    BaseUnitRepo,
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)
from bushidolib.unit.cardio import build_cardio_unit
from bushidolib.unit.martial_arts import build_gym_unit
from bushidolib.unit.strength import (
    build_lifting_unit,
)
from bushidolib.category.wimhof import build_wimhof_unit
from bushidolib.constants import UnitCategory
from bushidolib.unit.base import BaseUnit, RawUnit


@dataclass(frozen=True)
class UnitSpec:
    unit_repo: type[BaseUnitRepo[Any, Any]]
    build_unit: Callable[[RawUnit, datetime.datetime], BaseUnit]


CATEGORY_REGISTRY: dict[UnitCategory, UnitSpec] = {
    UnitCategory.CARDIO: UnitSpec(
        unit_repo=CardioUnitRepo, build_unit=build_cardio_unit
    ),
    UnitCategory.GYM: UnitSpec(unit_repo=GymUnitRepo, build_unit=build_gym_unit),
    UnitCategory.LIFTING: UnitSpec(
        unit_repo=LiftingUnitRepo, build_unit=build_lifting_unit
    ),
    UnitCategory.WIMHOF: UnitSpec(
        unit_repo=WimhofUnitRepo, build_unit=build_wimhof_unit
    ),
}
