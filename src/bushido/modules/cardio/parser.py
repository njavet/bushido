from bushido.core.dtypes import ParsedUnit
from bushido.core.result import Err, Ok, Result
from bushido.modules.parser import UnitParser
from bushido.parsing.utils import parse_military_time_string, time_string_to_seconds

from .domain import CardioSpec


class CardioParser(UnitParser[CardioSpec]):
    def _parse_unit(self) -> Result[ParsedUnit[CardioSpec]]:
        if not self.tokens:
            return Err("empty payload")

        res_t = parse_military_time_string(self.tokens[0])
        if isinstance(res_t, Err):
            return res_t

        start_t = res_t.value
        res_s = time_string_to_seconds(self.tokens[1])
        if isinstance(res_s, Err):
            return Err("no time")

        seconds = res_s.value
        try:
            location = self.tokens[2]
        except IndexError:
            return Err("no location")

        try:
            distance = float(self.tokens[3])
        except IndexError:
            distance = None
        try:
            avg_hr = int(self.tokens[4])
        except IndexError:
            avg_hr = None
        try:
            max_hr = int(self.tokens[5])
        except IndexError:
            max_hr = None
        try:
            calories = int(self.tokens[6])
        except IndexError:
            calories = None

        pu = ParsedUnit(
            name=self.unit_name,
            data=CardioSpec(
                start_t=start_t,
                seconds=seconds,
                location=location,
                distance=distance,
                avg_hr=avg_hr,
                max_hr=max_hr,
                calories=calories,
            ),
            log_time=self.log_time,
            comment=self.comment,
        )
        return Ok(pu)
