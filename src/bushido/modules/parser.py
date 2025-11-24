import datetime
from abc import ABC, abstractmethod
from typing import Generic

from bushido.modules.dtypes import Err, Ok, ParsedUnit, Result, TUData


class UnitParser(ABC, Generic[TUData]):
    def __init__(self, unit_name: str) -> None:
        self.unit_name = unit_name
        self.tokens: list[str] = []
        self.comment: str | None = None
        self.payload: str | None = None
        self.log_dt: datetime.datetime | None = None

    def _parse_comment(self, line: str) -> list[str]:
        """parses comment if present and returns list of tokens"""
        parts = line.split("#", 1)
        if len(parts) > 1 and parts[1]:
            self.comment = parts[1].strip()
        self.payload = parts[0].strip()
        return parts[0].split()

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
    def _parse_unit(self) -> Result[ParsedUnit[TUData]]: ...

    def parse(self, line: str) -> Result[ParsedUnit[TUData]]:
        tokens = self._parse_comment(line)

        dt_res = self._parse_log_dt(tokens)
        if isinstance(dt_res, Err):
            return dt_res

        self.tokens = dt_res.value
        return self._parse_unit()
