from dataclasses import dataclass
from typing import Generic, TypeVar, Literal, Union


T = TypeVar('T')

@dataclass
class Ok(Generic[T]):
    value: T
    kind: Literal['ok'] = 'ok'


@dataclass
class Err:
    message: str
    kind: Literal['err'] = 'err'


Result = Union[Ok[T], Err]
