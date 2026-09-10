import datetime

from pydantic import BaseModel

from bushidolib.constants import UnitCategory
from bushidolib.exceptions import UnitParsingError
from bushidolib.registry import UNIT_TYPE_REGISTRY, UnitData


class BaseUnit(BaseModel):
    name: str
    log_time: datetime.datetime
    comment: str | None = None


class RawUnit(BaseModel):
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None
