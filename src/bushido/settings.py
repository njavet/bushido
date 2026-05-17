from zoneinfo import ZoneInfo

from bushido.conf import UnitType

TIMEZONE = ZoneInfo("Europe/Zurich")

DAY_START_HOUR = 4


UNIT_SETTINGS = [
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
