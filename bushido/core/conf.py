from enum import StrEnum
from zoneinfo import ZoneInfo

DEFAULT_PORT = 8080

LOCAL_TIME_ZONE = ZoneInfo('Europe/Zurich')

DAY_START_HOUR = 4

DB_URL = 'sqlite:///bushido.db'


class UnitCategory(StrEnum):
    LIFTING = 'lifting'
    GYM = 'gym'


class LiftingUnitName(StrEnum):
    SQUAT = 'squat'
    DEADLIFT = 'deadlift'
    BENCHPRESS = 'benchpress'
    OVERHEADPRESS = 'overheadpress'
    ROWS = 'rows'


class GymUnitName(StrEnum):
    WEIGHTS = 'weights'
    MARTIAL_ARTS = 'martial_arts'
    YOGA = 'yoga'
