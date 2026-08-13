import datetime
from dataclasses import dataclass

from ..base import UnitSetting


@dataclass(frozen=True, slots=True)
class Data:
    start_t: datetime.time
    seconds: float
    location: str
    distance: float | None
    avg_hr: int | None
    max_hr: int | None
    calories: int | None


grammar = """
<name> <start> <sec> <loc> [<dist>] [<avg_hr>] [<max_hr>] [<cal>] # [<comment>]
    """

unit_settings = [
    UnitSetting(
        name="running",
        emoji=b"\xf0\x9f\xaa\x96".decode(),
    ),
    UnitSetting(
        name="swimming",
        emoji=b"\xf0\x9f\xa6\x88".decode(),
    ),
    UnitSetting(
        name="skipping",
        emoji=b"\xf0\x9f\x8e\x97\xef\xb8\x8f".decode(),
    ),
]
