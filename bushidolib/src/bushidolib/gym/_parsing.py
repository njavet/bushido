from bushidolib.parsing import parse_start_end_time_string
from bushidolib.exceptions import UnitParsingError

from ._spec import GymData


def parse(tokens: tuple[str, ...]) -> GymData:
    start_t, end_t = parse_start_end_time_string(tokens[0])
    try:
        location = tokens[1]
    except IndexError as e:
        raise UnitParsingError("no location") from e

    return GymData(
        start_t=start_t,
        end_t=end_t,
        gym=location,
        training=None,
        focus=None,
    )
