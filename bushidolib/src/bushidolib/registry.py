from collections.abc import Callable

from bushidolib.category.cardio import parse_cardio_data
from bushidolib.category.gym import parse_gym_data
from bushidolib.category.lifting import parse_lifting_data
from bushidolib.category.wimhof import parse_wimhof_data
from bushidolib.constants import UnitCategory

UNIT_TYPE_REGISTRY: dict[UnitCategory, Callable[[tuple[str, ...]], object]] = {
    UnitCategory.CARDIO: parse_cardio_data,
    UnitCategory.GYM: parse_gym_data,
    UnitCategory.LIFTING: parse_lifting_data,
    UnitCategory.WIMHOF: parse_wimhof_data,
}
