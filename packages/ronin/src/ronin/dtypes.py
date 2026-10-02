from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class UnitLogResult:
    unit: Any | None = None
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.unit is not None
