from dataclasses import dataclass


@dataclass
class RoundSpec:
    round_nr: int
    breaths: int
    retention: int


@dataclass
class WimhofSpec:
    rounds: list[RoundSpec]
