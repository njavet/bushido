from typing import Protocol


class UnitParser(Protocol):
    def parse(self, words: list[str], comment: str | None) -> ParsedUnit:
        ...
