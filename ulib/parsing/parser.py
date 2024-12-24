from abc import ABC


class BaseParser(ABC):
    def __init__(self):
        self.attrs = None

    def parse_words(self, words: list[str]) -> None:
        raise NotImplementedError
