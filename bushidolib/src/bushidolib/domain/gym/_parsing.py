from bushidolib.exceptions import ParsingUnitError

from ..dt_parse import parse_start_end_time_string
from ._spec import Data


def parse(tokens: tuple[str, ...]) -> Data:
    start_t, end_t = parse_start_end_time_string(tokens[0])
    try:
        location = tokens[1]
    except IndexError as e:
        raise ParsingUnitError("no location") from e

    return Data(
        start_t=start_t,
        end_t=end_t,
        gym=location,
        training=None,
        focus=None,
    )
