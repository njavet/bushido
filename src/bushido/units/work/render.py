
from .orm import WorkUnit


def format_work_unit(unit: WorkUnit) -> str:
    return unit.name
