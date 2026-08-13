import datetime
from dataclasses import dataclass

from ..base import UnitSetting


@dataclass(frozen=True, slots=True)
class Data:
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = None
    focus: str | None = None


grammar = """
    <name> <start>-<end> <location> [<training>] [<focus>] # [<comment>]

    time format:
      HHMM-HHMM
"""

unit_settings = [
    UnitSetting(
        name="kyokushin",
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
    ),
    UnitSetting(
        name="grappling",
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
    ),
    UnitSetting(
        name="boxing",
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
    ),
    UnitSetting(
        name="lifting",
        emoji=b"\xf0\x9f\xa6\x8d".decode(),
    ),
]
