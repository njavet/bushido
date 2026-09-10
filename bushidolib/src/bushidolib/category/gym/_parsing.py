from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import parse_start_end_time_string

from ._spec import GymData


def parse_gym_data(tokens: tuple[str, ...]) -> GymData:
    start_t, end_t = parse_start_end_time_string(tokens[0])
    try:
        gym = tokens[1]
    except IndexError as e:
        raise UnitParsingError("no gym") from e

    return GymData(
        start_t=start_t,
        end_t=end_t,
        gym=gym,
    )
