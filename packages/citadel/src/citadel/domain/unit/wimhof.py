import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field

from citadel.exceptions import UnitParsingError

from .base import BaseUnit, RawUnit, UnitType


class WimhofFlags(StrEnum):
    z = "zen_mode"


class WimhofOptions(StrEnum):
    guide = "guide"


class RoundData(BaseModel):
    round_nr: int = Field(ge=0)
    breaths: int = Field(ge=0)
    retention: int = Field(ge=0, lt=600)


class WimhofUnit(BaseUnit):
    unit_type: Literal[UnitType.wimhof] = UnitType.wimhof
    rounds: list[RoundData]
    zen_mode: bool = False
    guide: str | None = None


def parse_round_data(tokens: tuple[str, ...]) -> list[RoundData]:
    breaths = [int(b) for b in tokens[::2]]
    retentions = [int(r) for r in tokens[1::2]]
    if len(breaths) == 0:
        raise UnitParsingError("at least one round")
    if len(breaths) != len(retentions):
        raise UnitParsingError(f"breaths and retentions don't match {tokens}")
    if any(x < 0 for x in breaths):
        raise UnitParsingError("breaths must all be positive")
    if any(x < 0 for x in retentions):
        raise UnitParsingError("retentions must all be positive")

    return [
        RoundData(round_nr=i, breaths=b, retention=r)
        for i, (b, r) in enumerate(zip(breaths, retentions, strict=False))
    ]


def build_wimhof_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> WimhofUnit:
    rounds = parse_round_data(raw_unit.tokens)
    return WimhofUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        rounds=rounds,
        zen_mode=WimhofFlags.z in raw_unit.flags,
        guide=raw_unit.options.get(WimhofOptions.guide, None),
    )
