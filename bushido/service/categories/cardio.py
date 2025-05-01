# project imports
from bushido.exceptions import ValidationError
from bushido.utils.parsing import (parse_military_time_string,
                                   parse_time_string)
from bushido.data.categories.cardio import KeikoModel


def create_keiko(words):
    start_t = parse_military_time_string(words[0])
    seconds = parse_time_string(words[1])
    try:
        gym = words[2]
    except IndexError:
        raise ValidationError('no gym')

    try:
        distance = float(words[3])
    except (ValueError, IndexError):
        distance = None

    keiko = KeikoModel(start_t=start_t,
                       seconds=seconds,
                       gym=gym,
                       distance=distance)
    return keiko
