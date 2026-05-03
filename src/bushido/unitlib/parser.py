import datetime
from dataclasses import abstractmethod, dataclass
from typing import Generic, TypeVar

UnitData = TypeVar("UnitData")


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[UnitData]):
    name: str
    data: UnitData
    log_time: datetime.datetime
    comment: str | None = None


@dataclass(frozen=True, slots=True)
class RawUnitData:
    tokens: list[str]
    comment: str | None = None


@dataclass(frozen=True, slots=True)
class BaseUnitParser(Generic[UnitData]):
    @staticmethod
    def preprocess(line: str) -> RawUnitData:
        parts = line.split("#", 1)
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        if parts:
            tokens = parts[0].split()
        else:
            tokens = []
        return RawUnitData(tokens=tokens, comment=comment)

    @abstractmethod
    def parse_unit_data(self) -> UnitData: ...

    def parse(self, line: str) -> ParsedUnit[UData]:
        raw_unit_data = self.preprocess(line)

        dt_res = self._parse_log_dt(tokens)
        if isinstance(dt_res, Err):
            return dt_res

        self.tokens = dt_res.value
        return self._parse_unit()
