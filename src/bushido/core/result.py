from dataclasses import dataclass
from typing import Generic, Literal, TypeVar, Union

T = TypeVar("T")


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T
    kind: Literal["ok"] = "ok"


@dataclass(frozen=True)
class Warn:
    message: str
    kind: Literal["warning"] = "warning"


@dataclass(frozen=True)
class Err:
    message: str
    kind: Literal["err"] = "err"


Result = Union[Ok[T], Err]
