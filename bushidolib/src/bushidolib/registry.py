from collections.abc import Callable
from dataclasses import dataclass

from bushidolib.constants import UnitCategory
from bushidolib.unit import BaseUnit
from bushidolib.cardio import CardioData, CardioUnit, parse_cardio_unit
from bushidolib.gym import GymData, GymUnit, parse_gym_unit
from bushidolib.lifting import LiftingData, LiftingUnit, parse_lifting_unit
from bushidolib.wimhof import WimhofData, WimhofUnit, parse_wimhof_unit


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