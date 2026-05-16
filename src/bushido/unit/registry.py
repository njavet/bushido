from dataclasses import dataclass
from typing import Any

from bushido.unit.base import Mapper


@dataclass(frozen=True, slots=True)
class UnitRegistry:
    mapper: Mapper[Any, Any]

