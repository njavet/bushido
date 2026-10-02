import datetime
from typing import Self

from pydantic import BaseModel, Field

from bushidolib.constants import COMMENT_SEP
from bushidolib.exceptions import UnitParsingError
from bushidolib.parsing import split_words







class BaseUnit(BaseModel):
    log_time: datetime.datetime
    comment: str | None = None


class SpaceTimeData(BaseModel):
    start_t: datetime.time
    end_t: datetime.time
    gym: str
