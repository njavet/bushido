from bushido.domain.base import Err, Ok, ParsedUnit, Result
from bushido.domain.gym import GymSpec, GymUnitName
from bushido.iface.parser.unit import UnitParser
from bushido.iface.parser.utils import parse_start_end_time_string


class GymParser(UnitParser[GymSpec]):
    def _parse_unit_name(self, tokens: list[str]) -> Result[list[str]]:
        if len(tokens) == 0:
            return Err("no unit name")
        if tokens[0] not in [u.name for u in GymUnitName]:
            return Err("invalid unit name")
        self.unit_name = tokens[0]
        return Ok(tokens[1:])

    def _parse_unit(self) -> Result[ParsedUnit[GymSpec]]:
        res_t = parse_start_end_time_string(self.tokens[0])
        if isinstance(res_t, Err):
            return res_t

        start_t, end_t = res_t.value
        try:
            location = self.tokens[1]
        except IndexError:
            return Err("invalid unit location")
        try:
            training = self.tokens[2]
        except IndexError:
            training = None
        try:
            focus = self.tokens[3]
        except IndexError:
            focus = None

        pu = ParsedUnit(
            name=self.unit_name,
            data=GymSpec(
                start_t=start_t,
                end_t=end_t,
                location=location,
                training=training,
                focus=focus,
            ),
            comment=self.comment,
            log_dt=self.log_dt,
        )
        return Ok(pu)
