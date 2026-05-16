from dataclasses import dataclass
from typing import Any

from bushido.unit.base import Mapper, Parser


@dataclass(frozen=True, slots=True)
class UnitRegistry:
    parser: Parser[Any]
    mapper: Mapper[Any, Any]
