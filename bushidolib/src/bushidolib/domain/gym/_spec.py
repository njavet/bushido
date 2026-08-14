import datetime
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Data:
    start_t: datetime.time
    end_t: datetime.time
    gym: str
    training: str | None = None
    focus: str | None = None


grammar = """
    <name> <start>-<end> <location> [<training>] [<focus>] # [<comment>]

    time format:
      HHMM-HHMM
"""
