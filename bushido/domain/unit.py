from typing import Protocol
from dataclasses import dataclass

# project imports
from bushido.core.result import Result
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


class UnitParser(Protocol):
    def parse(self, words: list[str], comment: str | None) -> Result[ParsedUnit]:
        ...


class UnitStore(Protocol):
    def store(self, parsed_init: ParsedUnit) -> Result[int]:
        ...
