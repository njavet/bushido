from dataclasses import dataclass
from zoneinfo import ZoneInfo

from bushido.conf import UnitType

TIMEZONE = ZoneInfo("Europe/Zurich")

DAY_START_HOUR = 4


@dataclass(frozen=True, slots=True)
class UnitSetting:
    name: str
    emoji: str
    unit_type: UnitType


UNIT_SETTINGS = [
    UnitSetting(
        name="kyokushin",
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
        unit_type=UnitType.GYM,
    ),
    UnitSetting(
        name="grappling",
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
        unit_type=UnitType.GYM,
    ),
    UnitSetting(
        name="boxing",
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
        unit_type=UnitType.GYM,
    ),
    UnitSetting(
        name="lifting",
        emoji=b"\xf0\x9f\xa6\x8d".decode(),
        unit_type=UnitType.GYM,
    ),
    UnitSetting(
        name="squat",
        emoji=b"\xe2\x9b\xa9\xef\xb8\x8f".decode(),
        unit_type=UnitType.LIFTING,
    ),
    UnitSetting(
        name="deadlift",
        emoji=b"\xf0\x9f\x8f\x97\xef\xb8\x8f".decode(),
        unit_type=UnitType.LIFTING,
    ),
    UnitSetting(
        name="benchpress",
        emoji=b"\xf0\x9f\x9b\xab".decode(),
        unit_type=UnitType.LIFTING,
    ),
    UnitSetting(
        name="overheadpress",
        emoji=b"\xf0\x9f\x9a\x81".decode(),
        unit_type=UnitType.LIFTING,
    ),
    UnitSetting(
        name="rows",
        emoji=b"\xf0\x9f\x90\xa2".decode(),
        unit_type=UnitType.LIFTING,
    ),
    UnitSetting(
        name="curls",
        emoji=b"\xf0\x9f\xa6\xbe".decode(),
        unit_type=UnitType.LIFTING,
    ),
    UnitSetting(
        name="wimhof",
        emoji=b"\xf0\x9f\xaa\x90".decode(),
        unit_type=UnitType.WIMHOF,
    ),
    UnitSetting(
        name="running",
        emoji=b"\xf0\x9f\xaa\x96".decode(),
        unit_type=UnitType.CARDIO,
    ),
    UnitSetting(
        name="swimming",
        emoji=b"\xf0\x9f\xa6\x88".decode(),
        unit_type=UnitType.CARDIO,
    ),
    UnitSetting(
        name="skipping",
        emoji=b"\xf0\x9f\x8e\x97\xef\xb8\x8f".decode(),
        unit_type=UnitType.CARDIO,
    ),
]
