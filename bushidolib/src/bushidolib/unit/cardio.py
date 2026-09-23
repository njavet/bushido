import datetime
from enum import StrEnum

from pydantic import BaseModel

from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import (
    parse_military_time_string,
    time_string_to_seconds,
)
from bushidolib.unit.base import BaseUnit, RawUnit


class CardioType(StrEnum):
    running = "running"
    swimming = "swimming"
    skipping = "skipping"


class CardioData(BaseModel):
    start_t: datetime.time
    seconds: float
    gym: str
    avg_hr: int | None = None
    max_hr: int | None = None
    calories: int | None = None


class RunningUnit(BaseUnit, CardioData):
    distance: float


class SwimmingUnit(BaseUnit, CardioData):
    distance: float
    pool_length: int | None = None
    temperature: float | None = None


class RopeSkipUnit(BaseUnit, CardioData):
    pass


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


CardioUnit = RunningUnit | SwimmingUnit | RopeSkipUnit


def build_cardio_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> CardioUnit:
    data = parse_cardio_data(raw_unit.tokens, raw_unit.options)
    match raw_unit.name:
        case CardioType.running:
            try:
                distance = float(raw_unit.tokens[3])
            except KeyError, ValueError:
                raise UnitParsingError(f"wrong distance {raw_unit.tokens}")
            return RunningUnit(
                log_time=log_time,
                comment=raw_unit.comment,
                start_t=data.start_t,
                seconds=data.seconds,
                gym=data.gym,
                distance=distance,
                avg_hr=data.avg_hr,
                max_hr=data.max_hr,
                calories=data.calories,
            )
        case CardioType.swimming:
            try:
                distance = float(raw_unit.tokens[3])
            except KeyError, ValueError:
                raise UnitParsingError(f"wrong distance {raw_unit.tokens}")
            try:
                pool_length = raw_unit.options["pl"]
            except KeyError, ValueError:
                pool_length = None
            try:
                temperature = raw_unit.options["tmp"]
            except KeyError, ValueError:
                temperature = None
            return SwimmingUnit(
                log_time=log_time,
                comment=raw_unit.comment,
                start_t=data.start_t,
                seconds=data.seconds,
                gym=data.gym,
                distance=distance,
                pool_length=pool_length,
                temperature=temperature,
                avg_hr=data.avg_hr,
                max_hr=data.max_hr,
                calories=data.calories,
            )
        case CardioType.skipping:
            return RopeSkipUnit(
                log_time=log_time,
                comment=raw_unit.comment,
                start_t=data.start_t,
                seconds=data.seconds,
                gym=data.gym,
                avg_hr=data.avg_hr,
                max_hr=data.max_hr,
                calories=data.calories,
            )
        case _:
            raise UnitParsingError(f"no such unit {raw_unit.name}")
