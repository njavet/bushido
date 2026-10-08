import datetime
from typing import Literal

from pydantic import BaseModel

from citadel.exceptions import UnitParsingError

from citadel.unit.base import BaseUnit, RawUnit, UnitType
from citadel.unit.parsing import (
    parse_military_time_string,
    time_string_to_seconds,
)


class CardioData(BaseModel):
    start_t: datetime.time
    seconds: float
    gym: str
    avg_hr: int | None = None
    max_hr: int | None = None
    calories: int | None = None


def parse_cardio_data(tokens: tuple[str, ...], options: dict[str, str]) -> CardioData:
    start_t = parse_military_time_string(tokens[0])
    seconds = time_string_to_seconds(tokens[1])
    try:
        gym = tokens[2]
    except IndexError as e:
        raise UnitParsingError("no gym") from e
    try:
        avg_hr = int(options["avg_hr"])
    except KeyError:
        avg_hr = None
    try:
        max_hr = int(options["max_hr"])
    except KeyError:
        max_hr = None
    try:
        calories = int(options["cal"])
    except KeyError:
        calories = None
    return CardioData(
        start_t=start_t,
        seconds=seconds,
        gym=gym,
        avg_hr=avg_hr,
        max_hr=max_hr,
        calories=calories,
    )
