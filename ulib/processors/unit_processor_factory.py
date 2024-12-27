from abc import ABC


class UnitProcessorFactory(ABC):
    def __init__(self):
        self.attrs = None

    def parse_unit(self, words, comment) -> str:
        try:
            self.process_words(words)
        except ValueError:
            return 'wrong format'

    def process_words(self, words: list[str]) -> None:
        raise NotImplementedError
