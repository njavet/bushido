import datetime
from abc import ABC, abstractmethod
from typing import Generic

from bushido.modules.base import Err, Ok, ParsedUnit, Result, UnitData


class UnitParser(ABC, Generic[UnitData]):
    def __init__(self) -> None:
        self.unit_name: str
        self.tokens: list[str] = []
        self.comment: str | None = None
        self.log_dt: datetime.datetime | None = None

    def _parse_comment(self, line: str) -> list[str]:
        parts = line.split("#", 1)
        if len(parts) > 1 and parts[1]:
            self.comment = parts[1].strip()
        return parts[0].split()

    @abstractmethod
    def _parse_unit_name(self, tokens: list[str]) -> Result[list[str]]: ...

    def _parse_log_dt(self, tokens: list[str]) -> Result[list[str]]:
        try:
            index = tokens.index("--dt")
        except ValueError:
            return Ok(tokens)
        try:
            dt = tokens[index + 1].strip()
        except IndexError:
            return Err("no dt")
        try:
            self.log_dt = datetime.datetime.strptime(dt, "%Y%m%d-%H%M")
        except ValueError:
            return Err("invalid dt")

        return Ok(tokens[:index] + tokens[index + 2 :])

    @abstractmethod
    def _parse_unit(self) -> Result[ParsedUnit[UnitData]]: ...

    def parse(self, line: str) -> Result[ParsedUnit[UnitData]]:
        tokens = self._parse_comment(line)

        u_res = self._parse_unit_name(tokens)
        if isinstance(u_res, Err):
            return u_res

        dt_res = self._parse_log_dt(u_res.value)
        if isinstance(dt_res, Err):
            return dt_res

        self.tokens = dt_res.value
        return self._parse_unit()
