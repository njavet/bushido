from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoundData:
    round_nr: int
    breaths: int
    retention: int


@dataclass(frozen=True, slots=True)
class Data:
    rounds: list[RoundData]


grammar = "<name> (<breaths> <retentions>)+ # [<comment>]"
