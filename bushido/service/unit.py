from collections import defaultdict

# project imports
from bushido.schema.res import UnitLogResponse
from bushido.utils.helpers import load_unit_services
from bushido.utils.dt_functions import create_unit_response_dt
from bushido.utils.parsing import (preprocess_input,
                                   parse_datetime_to_timestamp)
from bushido.data.base_models import UnitModel
from bushido.data.repo import Repository


class BaseUnitService:
    def __init__(self, repo: Repository):
        self.repo = repo
        self.unit_services = load_unit_services()

    @classmethod
    def from_session(cls, session):
        return cls(Repository(session))

    def get_all_categories(self):
        categories = self.repo.get_all_categories()
        return [dict(key=r.name, value=r.name) for r in categories]

    def get_all_emojis(self):
        rows = self.repo.get_all_emojis()
        return [dict(key=r.unit_name, value=r.emoji) for r in rows]

    def get_emoji_for_unit(self, unit_name):
        emoji = self.repo.get_emoji_for_unit(unit_name)
        return emoji

    def get_all_units(self,
                  unit_name=None,
                  start_t=None,
                  end_t=None,
                  keiko_mode=None):
        units = self.repo.get_units(unit_name, start_t, end_t, keiko_mode)
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

    def log_unit(self, text):
        emoji, words, comment = preprocess_input(text)
        timestamp, words = parse_datetime_to_timestamp(words)
        bushido_date, hms = create_unit_response_dt(timestamp)
        unit_name = self.repo.get_unit_name_for_emoji(emoji)
        category = self.repo.get_category_for_unit(unit_name)
        unit_service = self.unit_services[category](self.repo)
        unit_service.process_unit(unit_name, words, timestamp, comment)
        return UnitLogResponse(date=bushido_date,
                               hms=hms,
                               emoji=emoji,
                               unit_name=unit_name,
                               payload=' '.join(words))

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
