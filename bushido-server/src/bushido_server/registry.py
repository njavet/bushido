from collections.abc import Callable

from bushidolib.category.cardio import CardioData, parse_cardio_data
from bushidolib.category.gym import GymData, parse_gym_data
from bushidolib.category.lifting import LiftingData, parse_lifting_data
from bushidolib.category.wimhof import WimhofData, parse_wimhof_data
from bushidolib.constants import UnitCategory

UnitData = CardioData | GymData | LiftingData | WimhofData

UNIT_TYPE_REGISTRY: dict[UnitCategory, Callable[[tuple[str, ...]], UnitData]] = {
    UnitCategory.CARDIO: parse_cardio_data,
    UnitCategory.GYM: parse_gym_data,
    UnitCategory.LIFTING: parse_lifting_data,
    UnitCategory.WIMHOF: parse_wimhof_data,
}
