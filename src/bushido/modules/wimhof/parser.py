from bushido.modules.domain import Err, Ok, ParsedUnit, Result
from bushido.modules.orm import UnitParser
from bushido.modules.wimhof.domain import RoundSpec, WimhofSpec, WimhofUnitName


class WimhofParser(UnitParser[WimhofSpec]):
    def _parse_unit_name(self, tokens: list[str]) -> Result[list[str]]:
        if len(tokens) == 0:
            return Err("no unit name")
        if tokens[0] not in [u.name for u in WimhofUnitName]:
            return Err("invalid unit name")
        self.unit_name = tokens[0]
        return Ok(tokens[1:])

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
            log_dt=self.log_dt,
        )
        return Ok(pu)
