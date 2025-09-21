# project imports
from bushido.core.result import Result
from bushido.domain.base import ParsedUnit
from bushido.service.parser.base import UnitParser


class LiftingParser(UnitParser):
    def parse(self, words: list[str], comment: str | None) -> Result[ParsedUnit]:
        ...
