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
]
