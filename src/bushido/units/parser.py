import datetime
from dataclasses import dataclass

from bushido.core.result import Err, Ok, Result


@dataclass(frozen=True, slots=True)
class BaseUnitParser:
    @staticmethod
    def _parse_comment(line: str) -> list[str]:
        parts = line.split("#", 1)
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        if parts:
            tokens = parts[0].split()
        else:
            tokens = []
        return tokens

    def _parse_log_dt(self, tokens: list[str]) -> Result[list[str]]:
        try:
            index = tokens.index("--dt")
        except ValueError:
            self.log_time = datetime.datetime.now(datetime.timezone.utc)
            return Ok(tokens)
        try:
            dt = tokens[index + 1].strip()
        except IndexError:
            return Err("no dt")
        try:
            self.log_time = datetime.datetime.strptime(dt, "%Y%m%d-%H%M")
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
