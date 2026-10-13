from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LogUnitCommand:
    unit_name: str
    body: str
    comment: str | None = None
