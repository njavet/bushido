import datetime
from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class UnitLogRequest(BaseModel):
    name: str
    tokens: tuple[str, ...]
    log_time: datetime.datetime
    comment: str | None = None


@dataclass(frozen=True, slots=True)
class Unit(Generic[T]):
    name: str
    emoji: str
    log_time: datetime.datetime
    comment: str | None
    data: T
