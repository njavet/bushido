import datetime
from collections.abc import Callable
from dataclasses import dataclass

from bushido_server.persistence.repos import BaseUnitRepo, CardioUnitRepo, GymUnitRepo, LiftingUnitRepo, WimhofUnitRepo
from bushidolib.category.base import BaseUnit, RawUnit
from bushidolib.category.cardio import CardioData, parse_cardio_data, build_cardio_unit
from bushidolib.category.gym import GymData, parse_gym_data, build_gym_unit
from bushidolib.category.lifting import LiftingData, parse_lifting_data, build_lifting_unit
from bushidolib.category.wimhof import WimhofData, parse_wimhof_data, build_wimhof_unit
from bushidolib.constants import UnitCategory


@dataclass(frozen=True)
class UnitSpec:
    unit_repo: type[BaseUnitRepo]
    build_unit: Callable[[RawUnit, datetime.datetime], BaseUnit]


CATEGORY_REGISTRY: dict[UnitCategory, UnitSpec] = {
    UnitCategory.CARDIO: UnitSpec(unit_repo=CardioUnitRepo, build_unit=build_cardio_unit),
    UnitCategory.GYM: UnitSpec(unit_repo=GymUnitRepo, build_unit=build_gym_unit),
    UnitCategory.LIFTING: UnitSpec(unit_repo=LiftingUnitRepo, build_unit=build_lifting_unit),
    UnitCategory.WIMHOF: UnitSpec(unit_repo=WimhofUnitRepo, build_unit=build_wimhof_unit),
}
