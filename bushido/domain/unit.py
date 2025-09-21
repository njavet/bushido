from dataclasses import dataclass

# project imports
from bushido.core.unit import UnitName


@dataclass
class UnitSpec:
    unit_name: str
    words: list[str]
    comment: str | None = None


@dataclass
class ParsedUnit:
    unit_name: UnitName
    data: dict
    comment: str | None = None

