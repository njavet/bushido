from bushido.core.conf import GymUnitName
from bushido.core.result import Err, Ok, Result
from bushido.domain.gym import GymSpec
from bushido.domain.unit import ParsedUnit, UnitSpec
from bushido.iface.parser.utils import parse_start_end_time_string


class GymParser:
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit[GymSpec]]:
        if unit_spec.name not in [u.name for u in GymUnitName]:
            return Err('invalid unit name')

        res_t = parse_start_end_time_string(unit_spec.words[0])
        if isinstance(res_t, Err):
            return res_t

        start_t, end_t = res_t.value
        try:
            focus = unit_spec.words[2]
        except IndexError:
            focus = None

        pu = ParsedUnit(
            name=unit_spec.name,
            data=GymSpec(
                start_t=start_t,
                end_t=end_t,
                location=unit_spec.words[1],
                focus=focus,
            ),
            comment=unit_spec.comment,
        )
        return Ok(pu)
