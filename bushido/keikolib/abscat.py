from typing import Dict
from dataclasses import dataclass, field
from collections import defaultdict
from abc import ABC


class AbsProcessor(ABC):
    def __init__(self) -> None:
        self.attrs = None

    def process_unit(self, unix_timestamp, words, comment):
        self._process_words(words)
        unit = self._save_unit(unix_timestamp)

        self._save_message(unit, words, comment)
        self._save_keiko(unit)

    def _process_words(self, words: list[str]):
        raise NotImplementedError

    def _save_unit(self, unix_timestamp) -> Unit:
        unit = Unit.create(category=self.category,
                           uname=self.uname,
                           umoji=self.umoji,
                           unix_timestamp=unix_timestamp)
        return unit

    @staticmethod
    def _save_message(unit, words, comment):
        Message.create(unit=unit,
                       payload=' '.join(words),
                       comment=comment)
