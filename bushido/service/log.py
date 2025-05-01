# project imports
from bushido.schema.res import UnitResponse
from bushido.utils.dtf import create_unit_response_dt
from bushido.utils.parsing import (preprocess_input,
                                   parse_datetime_to_timestamp)
from bushido.data.base_models import UnitModel
from bushido.data.repo import Repository
from bushido.service.loader import load_log_service


class LogService:
    def __init__(self, repo: Repository):
        self.repo = repo

    @classmethod
    def from_session(cls, session):
        return cls(Repository(session))

    def log_unit(self, text):
        emoji, words, comment = preprocess_input(text)
        timestamp, words = parse_datetime_to_timestamp(words)
        bushido_date, hms = create_unit_response_dt(timestamp)
        unit_name = self.repo.get_unit_name_for_emoji(emoji)
        category = self.repo.get_category_for_unit(unit_name)
        create_keiko = load_log_service(category)
        self.process_unit(unit_name,
                          words,
                          timestamp,
                          create_keiko,
                          comment)
        return UnitResponse(date=bushido_date,
                            hms=hms,
                            emoji=emoji,
                            unit_name=unit_name,
                            payload=' '.join(words))

    def process_unit(self,
                     unit_name,
                     words,
                     timestamp,
                     create_keiko,
                     comment=None):
        unit = self.create_unit(unit_name, words, timestamp, comment)
        unit_key = self.repo.save_unit(unit)
        keiko = create_keiko(words)
        self.repo.save_keiko(unit_key, keiko)

    def create_unit(self, unit_name, words, timestamp, comment=None):
        emoji_key = self.repo.get_emoji_key_by_unit(unit_name)
        unit = UnitModel(timestamp=timestamp,
                         payload=' '.join(words),
                         comment=comment,
                         fk_emoji=emoji_key)
        return unit
