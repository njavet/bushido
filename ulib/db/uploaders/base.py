from abc import ABC

# project imports
from ulib.db.tables import UnitTable


class BaseUploader(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.unit = None

    def upload_unit(self, timestamp, payload, comment, emoji_key, attrs):
        self._create_unit(timestamp, payload, comment, emoji_key)
        self._upload_unit(attrs)

    def _create_unit(self, timestamp, payload, comment, emoji_key):
        self.unit = UnitTable(timestamp=timestamp,
                              payload=payload,
                              comment=comment,
                              fk_emoji=emoji_key)

    def _upload_unit(self, attrs):
        raise NotImplementedError
