from enum import StrEnum


class GymUnitName(StrEnum):
    kyokushin = "kyokushin"
    grappling = "grappling"
    lifting = "lifting"


class CardioUnitName(StrEnum):
    running = "running"
    skipping = "skipping"
    swimming = "swimming"


class LiftingUnitName(StrEnum):
    squat = "squat"
    deadlift = "deadlift"
    benchpress = "benchpress"
    overheadpress = "overheadpress"
    rows = "rows"
    curls = "curls"


class WimhofUnitName(StrEnum):
    wimhof = "wimhof"


class UnitCategory(StrEnum):
    cardio = "cardio"
    lifting = "lifting"
    work = "work"
    gym = "gym"
    wimhof = "wimhof"


DEFAULT_CATEGORIES: tuple[str, ...] = (
    "cardio",
    "lifting",
    "gym",
    "wimhof",
)
