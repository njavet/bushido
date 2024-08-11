import peewee as pw
from typing import Dict
from dataclasses import dataclass, field
from collections import defaultdict
from abc import ABC

# project imports
from bushido.keikolib.db import BaseModel, Unit, Message


class AbsCategory(ABC):
    def __init__(self, category: str):
        self.category = category
        self.keiko = None

    def retrieve_units(self, uname=None) -> list:
        query = (Unit
                 .select(Unit, self.keiko)
                 .join(self.keiko)
                 .where(Unit.category == self.category)
                 .order_by(Unit.timestamp.desc()))
        if uname:
            return [unit for unit in query if unit.uname == uname]
        else:
            return list(query)


class AbsProcessor(ABC):
    def __init__(self, category: str, uname: str, umoji: str) -> None:
        self.category = category
        self.uname = uname
        self.umoji = umoji
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

    def _save_keiko(self, unit):
        raise NotImplementedError


class Keiko(BaseModel):
    unit = pw.ForeignKeyField(Unit)


@dataclass
class AbsUmojis:
    umoji2uname: Dict[str, str]
    # needed for different sized byte encodings of some emojis
    emoji2umoji: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))
