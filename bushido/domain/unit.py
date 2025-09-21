from dataclasses import dataclass


@dataclass
class UnitSpec:
    unit_name: str
    words: list[str]
    comment: str | None = None