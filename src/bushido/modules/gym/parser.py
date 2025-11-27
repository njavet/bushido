from bushido.core.dtypes import ParsedUnit
from bushido.core.result import Err, Ok, Result
from bushido.modules.parser import UnitParser
from bushido.parsing.utils import parse_start_end_time_string

from .domain import GymSpec


class GymParser(UnitParser[GymSpec]):
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
            log_time=self.log_time,
            comment=self.comment,
        )
        return Ok(pu)
