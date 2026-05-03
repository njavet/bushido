from .orm import CardioUnit


def format_cardio_unit(unit: CardioUnit) -> str:
    return unit.name
