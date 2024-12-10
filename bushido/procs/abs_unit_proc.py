from abc import ABC
from sqlalchemy.orm import Session

# project imports
from bushido.db.models import Unit, Message


class AbsUnitProcessor(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.attrs = None

    def process_unit(self, unix_timestamp, words, comment, emoji_key) -> str:
        try:
            self._process_words(words)
        except ValueError:
            return 'wrong format'
        unit_key = self._upload_unit(unix_timestamp, emoji_key)
        payload = ' '.join(words)
        self._upload_message(payload, comment, unit_key)
        self._upload_keiko(unit_key)
        return 'Unit confirmed'

    def _process_words(self, words: list[str]) -> None:
        raise NotImplementedError

    def _upload_unit(self, unix_timestamp, emoji_key) -> int:
        unit = Unit(unix_timestamp=unix_timestamp, emoji=emoji_key)
        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            # TODO investigate not bound to a session error
            return unit.key

    def _upload_message(self, payload, comment, unit_key) -> None:
        msg = Message(payload=payload, comment=comment, unit=unit_key)
        with Session(self.engine) as session:
            session.add(msg)
            session.commit()

    def _upload_keiko(self, unit_key):
        raise NotImplementedError
