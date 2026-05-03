from .orm import WimhofUnit


def format_wimhof_unit(unit: WimhofUnit) -> str:
    return unit.name
