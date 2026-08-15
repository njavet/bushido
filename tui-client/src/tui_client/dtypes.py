from dataclasses import dataclass

from bushidolib.unit import BaseUnit


@dataclass(frozen=True, slots=True)
class UnitLogResult:
    unit: BaseUnit | None = None
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.unit is not None
