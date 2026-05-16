from dataclasses import replace
from typing import Callable, Iterable

from bushido.units.base import Unit
from bushido.units.lifting.unit import LiftingData, SetData


def compute_unit_pr(
    units: Iterable[Unit[LiftingData]],
    n: int,
    key_fn: Callable[[tuple[Unit[LiftingData], SetData]], tuple[float, float]],
) -> list[Unit[LiftingData]]:
    candidates = [(unit, set_) for unit in units for set_ in unit.data.sets]
    best = sorted(
        candidates,
        key=key_fn,
        reverse=True,
    )[:n]
    return [replace(unit, data=replace(unit.data, sets=[set_])) for unit, set_ in best]
