from dataclasses import dataclass
from typing import Any

from bushido.unit.base import UnitMapper, UnitParser


@dataclass(frozen=True, slots=True)
class UnitRegistry:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any]
