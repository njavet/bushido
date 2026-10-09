import datetime

from citadel.unit.base import RawUnit

from ._bilateral import BilateralUnit, parse_bilateral_set_data


def build_benchpress_unit(
    raw_unit: RawUnit, log_time: datetime.datetime
) -> BilateralUnit:
    sets = parse_bilateral_set_data(raw_unit.tokens)
    return BilateralUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        sets=sets,
        variant=raw_unit.options.get("variant", "default"),
    )
