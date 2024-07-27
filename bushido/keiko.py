import peewee as pw
from typing import Dict
from dataclasses import dataclass, field
from collections import defaultdict
from abc import ABC

# project imports
from bushido.db import BaseModel, Unit, Message


class Keiko(BaseModel):
    """ abstract base class for all keikos """
    unit_id = pw.ForeignKeyField(Unit)


class AbsHelper(ABC):
    def __init__(self, category: str):
        self.category = category


class AbsProcessor(ABC):
    def __init__(self, category: str, uname: str, umoji: str) -> None:
        self.category = category
        self.uname = uname
        self.umoji = umoji
        self.attrs: None | AbsAttrs = None

    def process_unit(self, budoka_id, timestamp, words, comment):
        self._process_words(words)
        unit = self._save_unit(budoka_id, timestamp)
        self._save_message(unit, words, comment)
        self._save_keiko(unit)

    def _process_words(self, words: list[str]):
        raise NotImplementedError

    def _save_unit(self, budoka_id, timestamp) -> Unit:
        unit = Unit.create(budoka_id=budoka_id,
                           category=self.category,
                           uname=self.uname,
                           umoji=self.umoji,
                           timestamp=timestamp)
        return unit

    @staticmethod
    def _save_message(unit, words, comment):
        Message.create(unit=unit,
                       payload=' '.join(words),
                       comment=comment)

    def _save_keiko(self, unit):
        raise NotImplementedError


class AbsRetriever(ABC):
    def __init__(self, keiko: Keiko):
        self.keiko = keiko

    def retrieve_units(self, budoka_id):
        query = (Unit
                 .select(Unit, self.keiko)
                 .where(Unit.budoka == budoka_id)
                 .join(self.keiko)
                 .order_by(Unit.timestamp.desc()))
        return query


@dataclass
class AbsAttrs:
    pass


@dataclass
class AbsUmojis:
    umoji2uname: Dict[str, str]
    # needed for different sized byte encodings of some emojis
    emoji2umoji: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))
