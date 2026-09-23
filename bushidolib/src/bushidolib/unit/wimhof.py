import datetime

from pydantic import BaseModel

from bushidolib.exceptions import UnitParsingError
from bushidolib.unit.base import BaseUnit, RawUnit


class WimhofRoundData(BaseModel):
    round_nr: int
    breaths: int
    retention: int


class WimhofData(BaseModel):
    rounds: list[WimhofRoundData]


class WimhofUnit(BaseUnit, WimhofData):
    zen_mode: bool = False
    guide: str | None = None


def parse_wimhof_data(tokens: tuple[str, ...]) -> WimhofData:
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

    return WimhofData(
        rounds=[
            WimhofRoundData(round_nr=i, breaths=b, retention=r)
            for i, (b, r) in enumerate(zip(breaths, retentions, strict=False))
        ]
    )


def build_wimhof_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> WimhofUnit:
    data = parse_wimhof_data(raw_unit.tokens)
    return WimhofUnit(
        log_time=log_time,
        comment=raw_unit.comment,
        rounds=data.rounds,
        # TODO rm hardcoding
        zen_mode='-z' in raw_unit.flags,
        guide=raw_unit.options.get('--guide', None)
    )
