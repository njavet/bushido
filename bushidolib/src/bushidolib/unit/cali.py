import datetime

from bushidolib.unit.base import BaseUnit, RawUnit


class CaliUnit(BaseUnit):
    pushups: int
    squats: int
    situps: int
    pullups: int


def build_cali_unit(raw_unit: RawUnit, log_time: datetime.datetime) -> CaliUnit:
    data = raw_unit.tokens[0].split(',')
    return CaliUnit(
        log_time=log_time,
        comment=raw_unit.comment,
        pushups=int(data[0]),
        squats=int(data[1]),
        situps=int(data[2]),
        pullups=int(data[3]),
    )

