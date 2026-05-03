from enum import StrEnum

from bushido.units.cardio import CardioUnitName
from bushido.units.gym import GymUnitName
from bushido.units.lifting import LiftingUnitName
from bushido.units.registry import REGISTRY, UnitRegistration
from bushido.units.wimhof import WimhofUnitName
from bushido.units.work import WorkUnitName


class UnitCategory(StrEnum):
    cardio = "cardio"
    lifting = "lifting"
    work = "work"
    gym = "gym"
    wimhof = "wimhof"


def unit_name_to_category(unit_name: str) -> UnitCategory:
    if unit_name in GymUnitName:
        return UnitCategory.gym
    elif unit_name in LiftingUnitName:
        return UnitCategory.lifting
    elif unit_name in WimhofUnitName:
        return UnitCategory.wimhof
    elif unit_name in CardioUnitName:
        return UnitCategory.cardio
    elif unit_name in WorkUnitName:
        return UnitCategory.work
    else:
        raise ValueError(f"Unknown unit: {unit_name}")


def get_registration(unit_name: str) -> UnitRegistration:
    category = unit_name_to_category(unit_name)
    return REGISTRY[category]
