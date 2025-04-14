import datetime
from bushido.conf import LOCAL_TIME_ZONE
from bushido.data.base_models import UnitModel
from bushido.data.unit import UnitRepository


class UnitService:
    def __init__(self, unit_repo):
        self.unit_repo = unit_repo

    @classmethod
    def from_session(cls, session):
        return cls(UnitRepository(session))

    def get_all_emojis(self):
        rows = self.unit_repo.get_all()
        return [dict(key=r.unit_name, value=r.emoji) for r in rows]

    def emoji_for_unit(self, unit_name: str):
        return self.unit_repo.get_emoji_for_unit(unit_name)

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        return self.unit_repo.get_units(unit_name, start_t, end_t)

    def get_category_for_unit(self, unit_name):
        return self.unit_repo.get_category_for_unit(unit_name)

    def process_unit(self, spec):
        unit = self.create_unit(spec)
        unit_key = self.unit_repo.save_unit(unit)
        keiko = self.create_keiko(spec.words)
        self.unit_repo.save_keiko(unit_key, keiko)

    def set_timestamp(self):
        now = datetime.datetime.now().replace(tzinfo=LOCAL_TIME_ZONE)
        timestamp = int(now.timestamp())
        return timestamp

    def create_unit(self, spec):
        emoji_key = self.unit_repo.get_emoji_key_by_unit(spec.unit_name)
        timestamp = self.set_timestamp()
        unit = UnitModel(timestamp=timestamp,
                         payload=' '.join(spec.words),
                         comment=spec.comment,
                         fk_emoji=emoji_key)
        return unit

    def create_keiko(self, words):
        raise NotImplementedError
