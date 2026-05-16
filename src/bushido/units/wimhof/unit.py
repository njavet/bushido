from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoundData:
    round_nr: int
    breaths: int
    retention: int


@dataclass(frozen=True, slots=True)
class WimhofData:
    rounds: list[RoundData]
