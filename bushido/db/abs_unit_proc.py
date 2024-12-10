from abc import ABC
from sqlalchemy.orm import Session

# project imports
from bushido.db.models import Unit, Message


class AbsUnitProcessor(ABC):
    def __init__(self, engine, emoji2key):
        self.engine = engine
        self.emoji2key = emoji2key
        self.payload = None
        self.comment = None

    def process_unit(self, unix_timestamp: float, input_str: str) -> str:
        try:
            self._preprocess_string(input_str)
        except ValueError as err:
            return str(err)

        all_words = self.payload.split()
        emoji = all_words[0]
        words = all_words[1:]
        try:
            emoji_key = self.emoji2key[emoji]
        except KeyError:
            return 'Unknown emoji'

        try:
            self._process_words(words)
        except ValueError:
            return 'wrong format'

        unit_key = self._upload_unit(unix_timestamp, emoji_key)
        self._upload_message(unit_key)
        self._upload_keiko(unit_key)

        return 'Unit confirmed'

    def _preprocess_string(self, input_str: str):
        parts = input_str.split('//', 1)
        self.payload = parts[0]

        if not self.payload:
            raise ValueError('Empty payload')

        if len(parts) > 1 and parts[1]:
            self.comment = parts[1].strip()
        else:
            self.comment = None

    def _process_words(self, words: list[str]):
        raise NotImplementedError

    def _upload_unit(self, unix_timestamp, emoji_key) -> int:
        unit = Unit(unix_timestamp=unix_timestamp, emoji=emoji_key)
        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
        return unit.key

    def _upload_message(self, unit_key):
        msg = Message(payload=self.payload, comment=self.comment, unit=unit_key)
        with Session(self.engine) as session:
            session.add(msg)
            session.commit()

    def _upload_keiko(self, unit_key):
        raise NotImplementedError
