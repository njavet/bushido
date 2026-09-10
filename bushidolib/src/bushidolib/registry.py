from collections.abc import Callable
from dataclasses import dataclass

from bushidolib.category.cardio import parse_cardio_data
from bushidolib.category.gym import parse_gym_data
from bushidolib.constants import UnitCategory
from bushidolib.category.lifting import parse_lifting_data
from bushidolib.category.wimhof import parse_wimhof_data


UNIT_TYPE_REGISTRY: dict[UnitCategory, Callable[[tuple[str, ...]], object]] = {
    UnitCategory.CARDIO: parse_cardio_data,
    UnitCategory.GYM: parse_gym_data,
    UnitCategory.LIFTING: parse_lifting_data,
    UnitCategory.WIMHOF: parse_wimhof_data,
}
