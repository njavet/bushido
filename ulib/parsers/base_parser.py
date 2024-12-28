from abc import ABC


class BaseParser(ABC):
    def __init__(self):
        pass

    def parse_words(self, words: list[str]):
        raise NotImplementedError
