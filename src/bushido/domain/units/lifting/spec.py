from dataclasses import dataclass

from ..base import UnitSetting


@dataclass(frozen=True, slots=True)
class SetData:
    set_nr: int
    weight: float
    reps: float
    rest: float


@dataclass(frozen=True, slots=True)
class Data:
    variant: str | None
    program: str | None
    sets: list[SetData]


grammar = """
<name> (<weight> <reps> [<rest>])+ -p <program> -v <variant> # [<comment>]
"""

unit_settings = [
    UnitSetting(
        name="squat",
        emoji=b"\xe2\x9b\xa9\xef\xb8\x8f".decode(),
    ),
    UnitSetting(
        name="deadlift",
        emoji=b"\xf0\x9f\x8f\x97\xef\xb8\x8f".decode(),
    ),
    UnitSetting(
        name="benchpress",
        emoji=b"\xf0\x9f\x9b\xab".decode(),
    ),
    UnitSetting(
        name="overheadpress",
        emoji=b"\xf0\x9f\x9a\x81".decode(),
    ),
    UnitSetting(
        name="rows",
        emoji=b"\xf0\x9f\x90\xa2".decode(),
    ),
    UnitSetting(
        name="curls",
        emoji=b"\xf0\x9f\xa6\xbe".decode(),
    ),
]
