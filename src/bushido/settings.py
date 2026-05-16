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
]
