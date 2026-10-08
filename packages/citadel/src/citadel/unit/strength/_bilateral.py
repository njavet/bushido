import datetime

from citadel.exceptions import UnitParsingError
from citadel.unit.base import RawUnit

from ._base import BilateralSet



def build_barbell_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> BarbellUnit:
    sets = parse_set_data(raw_unit.tokens)
    return BarbellUnit(
        name=raw_unit.name,
        log_time=log_time,
        comment=raw_unit.comment,
        sets=sets,
        variant=raw_unit.options.get("variant", "default"),
    )
