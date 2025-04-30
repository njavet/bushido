from abc import ABC, abstractmethod

# project imports
from bushido.data.base_models import UnitModel
from bushido.data.base_repo import BaseRepository


class AbsUnitService(ABC):
    def __init__(self, base_repo: BaseRepository):
        self.repo = base_repo

    @classmethod
    def from_session(cls, session):
        return cls(BaseRepository(session))

    def process_unit(self, unit_name, words, timestamp, comment=None):
        unit = self.create_unit(unit_name, words, timestamp, comment)
        unit_key = self.repo.save_unit(unit)
        keiko = self.create_keiko(words)
        self.repo.save_keiko(unit_key, keiko)

    def create_unit(self, unit_name, words, timestamp, comment=None):
        emoji_key = self.repo.get_emoji_key_by_unit(unit_name)
        unit = UnitModel(timestamp=timestamp,
                         payload=' '.join(words),
                         comment=comment,
                         fk_emoji=emoji_key)
        return unit

    @abstractmethod
    def create_keiko(self, words):
        raise NotImplementedError
