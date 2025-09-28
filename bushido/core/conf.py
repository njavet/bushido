from enum import StrEnum
from zoneinfo import ZoneInfo

DEFAULT_PORT = 8080

LOCAL_TIME_ZONE = ZoneInfo('Europe/Zurich')

DAY_START_HOUR = 4

DB_URL = 'sqlite:///bushido.db'


class UnitCategory(StrEnum):
    lifting = 'lifting'
    gym = 'gym'


class LiftingUnitName(StrEnum):
    squat = 'squat'
    deadlift = 'deadlift'
    benchpress = 'benchpress'
    overheadpress = 'overheadpress'
    rows = 'rows'


class GymUnitName(StrEnum):
    weights = 'weights'
    martial_arts = 'martial_arts'
    yoga = 'yoga'
