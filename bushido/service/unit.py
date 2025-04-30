from collections import defaultdict

# project imports
from bushido.schema.res import UnitLogResponse
from bushido.utils.dt_functions import create_unit_response_dt
from bushido.data.base_models import UnitModel
from bushido.data.repo import Repository


class BaseUnitService:
    def __init__(self, repo: Repository):
        self.repo = repo

    @classmethod
    def from_session(cls, session):
        return cls(Repository(session))

    def get_all_categories(self):
        with self.repo as repo:
            categories = repo.get_all_categories()
        return [dict(key=r.name, value=r.name) for r in categories]

    def get_all_emojis(self):
        with self.repo as repo:
            rows = repo.get_all_emojis()
        return [dict(key=r.unit_name, value=r.emoji) for r in rows]

    def get_emoji_for_unit(self, unit_name):
        with self.repo as repo:
            emoji = repo.get_emoji_for_unit(unit_name)
        return emoji

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        with self.repo as repo:
            units = repo.get_units(unit_name, start_t, end_t)
        dix = defaultdict(list)
        for unit in units:
            bushido_date, hms = create_unit_response_dt(unit.timestamp)
            ulr = UnitLogResponse(date=bushido_date,
                                  hms=hms,
                                  emoji=unit.emoji,
                                  unit_name=unit.unit_name,
                                  payload=unit.payload)
            dix[bushido_date].append(ulr)
            return dix

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

    def create_keiko(self, words):
        raise NotImplementedError
