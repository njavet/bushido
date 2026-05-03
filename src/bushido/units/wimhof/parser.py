from bushido.core.result import Err, Ok, Result
from bushido.units.parsing.base import UnitParser

from .domain import RoundSpec, WimhofSpec


class WimhofParser(UnitParser[WimhofSpec]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> Result[WimhofSpec]:
        breaths = [int(b) for b in tokens[::2]]
        retentions = [int(r) for r in tokens[1::2]]
        if len(breaths) == 0:
            return Err("at least one round")
        if len(breaths) != len(retentions):
            return Err("breaths and retentions don't match")
        if any(x < 0 for x in breaths):
            return Err("breaths must all be positive")
        if any(x < 0 for x in retentions):
            return Err("Retentions must all be positive")

        ex = WimhofSpec(
            rounds=[
                RoundSpec(round_nr=i, breaths=b, retention=r)
                for i, (b, r) in enumerate(zip(breaths, retentions))
            ]
        )
        return Ok(ex)
