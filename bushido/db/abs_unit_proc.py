from abc import ABC


class AbsUnitProcessor(ABC):
    def __init__(self):
        pass

    def process_unit(self, unix_timestamp, words, comment):
        pass