import datetime

from pydantic import BaseModel

from bushidolib.constants import UnitCategory


class UnitSetting(BaseModel):
    name: str
    category: UnitCategory


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    comment: str | None


class BaseUnit(BaseModel):
    name: str
    log_time: datetime.datetime
    comment: str | None



