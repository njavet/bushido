from dataclasses import dataclass
from typing import Generic, Literal, TypeVar, Union

RT = TypeVar('RT')


@dataclass(frozen=True)
class Ok(Generic[RT]):
    value: RT
    kind: Literal['ok'] = 'ok'


@dataclass(frozen=True)
class Err:
    message: str
    kind: Literal['err'] = 'err'


Result = Union[Ok[RT], Err]
