import datetime
from typing import Annotated

from pydantic import BaseModel, StringConstraints

LogLine = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=512,
    ),
]


class LogUnitRequest(BaseModel):
    line: LogLine


class LoadUnitRequest(BaseModel):
    unit_name: str
    start_t: datetime.datetime | None = None
    end_t: datetime.datetime | None = None
