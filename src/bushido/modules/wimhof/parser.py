from bushido.core.dtypes import ParsedUnit
from bushido.core.result import Err, Ok, Result
from bushido.modules.parser import UnitParser

from .domain import RoundSpec, WimhofSpec


class WimhofParser(UnitParser[WimhofSpec]):
    def _parse_unit(self) -> Result[ParsedUnit[WimhofSpec]]:
        breaths = [int(b) for b in self.tokens[::2]]
        retentions = [int(r) for r in self.tokens[1::2]]
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

        pu = ParsedUnit(
            name=self.unit_name,
            data=ex,
            comment=self.comment,
            log_time=self.log_time,
        )
        return Ok(pu)
