from abc import ABC, abstractmethod
import datetime
from bushido.utils.parsing import parse_option
from bushido.data.base_models import UnitModel
from bushido.data.base_repo import BaseRepository


class AbsLogService(ABC):
    def __init__(self, base_repo: BaseRepository):
        self.repo = base_repo

    @classmethod
    def from_session(cls, session):
        return cls(BaseRepository(session))

    def process_unit(self, unit_name, words, comment=None):
        unit = self.create_unit(unit_name, words, comment)
        unit_key = self.repo.save_unit(unit)
        keiko = self.create_keiko(words)
        self.repo.save_keiko(unit_key, keiko)

    def create_unit(self, unit_name, words, comment=None):
        emoji_key = self.repo.get_emoji_key_by_unit(unit_name)
        timestamp = self.parse_timestamp(words)
        unit = UnitModel(timestamp=timestamp,
                         payload=' '.join(words),
                         comment=comment,
                         fk_emoji=emoji_key)
        return unit

    @abstractmethod
    def create_keiko(self, words):
        raise NotImplementedError
