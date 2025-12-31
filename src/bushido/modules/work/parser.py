from bushido.core.dtypes import ParsedUnit
from bushido.core.result import Err, Ok, Result
from bushido.modules.parser import UnitParser
from bushido.parsing.utils import parse_start_end_time_string

from .domain import WorkSpec


class WorkParser(UnitParser[WorkSpec]):
    def _parse_unit(self) -> Result[ParsedUnit[WorkSpec]]:
        if not self.tokens:
            return Err("empty payload")

        res_t = parse_start_end_time_string(self.tokens[0])
        if isinstance(res_t, Err):
            return res_t

        start_t, end_t = res_t.value
        try:
            location = self.tokens[1]
        except IndexError:
            return Err("no unit location")
        try:
            employer = self.tokens[2]
        except IndexError:
            return Err("no unit employer")
        try:
            project = self.tokens[3]
        except IndexError:
            return Err("no unit project")

        pu = ParsedUnit(
            name=self.unit_name,
            data=WorkSpec(
                start_t=start_t,
                end_t=end_t,
                location=location,
                employer=employer,
                project=project,
            ),
            log_time=self.log_time,
            comment=self.comment,
        )
        return Ok(pu)
