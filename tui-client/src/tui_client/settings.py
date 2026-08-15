from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo

from bushidolib.constants import UnitCategory

LOCAL_TIMEZONE = ZoneInfo("Europe/Zurich")

BUSHIDO_IMG_PATH = Path(
    "tui-client", "src", "tui_client", "assets", "images", "bushido.png"
)


unit_emojis = {
    "squat": b"\xe2\x9b\xa9\xef\xb8\x8f".decode(),
    "deadlift": b"\xf0\x9f\x8f\x97\xef\xb8\x8f".decode(),
    "benchpress": b"\xf0\x9f\x9b\xab".decode(),
    "overheadpress": b"\xf0\x9f\x9a\x81".decode(),
    "rows": b"\xf0\x9f\x90\xa2".decode(),
    "curls": b"\xf0\x9f\xa6\xbe".decode(),
    "running": b"\xf0\x9f\xaa\x96".decode(),
    "swimming": b"\xf0\x9f\xa6\x88".decode(),
    "skipping": b"\xf0\x9f\x8e\x97\xef\xb8\x8f".decode(),
    "kyokushin": b"\xf0\x9f\xa5\x8b".decode(),
    "grappling": b"\xf0\x9f\xa5\x8b".decode(),
    "boxing": b"\xf0\x9f\xa5\x8b".decode(),
    "lifting": b"\xf0\x9f\xa6\x8d".decode(),
    "wimhof": b"\xf0\x9f\xaa\x90".decode(),
}


@dataclass(frozen=True, slots=True)
class UnitConf:
    emoji: str
    category: UnitCategory
