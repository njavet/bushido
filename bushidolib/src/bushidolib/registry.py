from collections.abc import Callable
from dataclasses import dataclass

from bushidolib.category.cardio import CardioUnit, parse_cardio_unit
from bushidolib.constants import UnitCategory
from bushidolib.gym import GymUnit, parse_gym_unit
from bushidolib.lifting import LiftingUnit, parse_lifting_unit
from bushidolib.unit import BaseUnit
from bushidolib.wimhof import WimhofUnit, parse_wimhof_unit


@dataclass(frozen=True)
class UnitTypeSpec:
    parse: Callable[[tuple[str, ...]], object]
    unit_cls: type[BaseUnit]


UNIT_TYPE_REGISTRY: dict[UnitCategory, UnitTypeSpec] = {
    UnitCategory.CARDIO: UnitTypeSpec(parse_cardio_unit, CardioUnit),
    UnitCategory.GYM: UnitTypeSpec(parse_gym_unit, GymUnit),
    UnitCategory.LIFTING: UnitTypeSpec(parse_lifting_unit, LiftingUnit),
    UnitCategory.WIMHOF: UnitTypeSpec(parse_wimhof_unit, WimhofUnit),
}
