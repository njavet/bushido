from abc import ABC


class ParserFactory(ABC):
    def __init__(self):
        self.attrs = None

    def parse_unit(self, words) -> str:
        try:
            self.parse_words(words)
        except ValueError:
            return 'wrong format'

    def parse_words(self, words: list[str]) -> None:
        raise NotImplementedError
