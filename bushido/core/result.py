from dataclasses import dataclass
from typing import Generic, Literal, Union

# project imports
from bushido.core.types import RT


@dataclass
class Ok(Generic[RT]):
    value: RT
    kind: Literal['ok'] = 'ok'


@dataclass
class Err:
    message: str
    kind: Literal['err'] = 'err'


Result = Union[Ok[RT], Err]
