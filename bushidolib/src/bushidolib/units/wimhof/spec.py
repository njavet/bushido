from dataclasses import dataclass

from ..base import UnitSetting


@dataclass(frozen=True, slots=True)
class RoundData:
    round_nr: int
    breaths: int
    retention: int


@dataclass(frozen=True, slots=True)
class Data:
    rounds: list[RoundData]


grammar = "<name> (<breaths> <retentions>)+ # [<comment>]"

unit_settings = [
    UnitSetting(
        name="wimhof",
        emoji=b"\xf0\x9f\xaa\x90".decode(),
    ),
]
