import datetime

from citadel.bcl import LogUnitCommand

from ._bilateral import BilateralUnit, parse_bilateral_set_data


def build_benchpress_unit(
    raw_unit: LogUnitCommand, log_time: datetime.datetime
) -> BilateralUnit:
    sets = parse_bilateral_set_data(raw_unit.args)
    return BilateralUnit(
        name=raw_unit.unit_name,
        log_time=log_time,
        comment=raw_unit.comment,
        sets=sets,
        variant=raw_unit.options.get("variant", "default"),
    )
