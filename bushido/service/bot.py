from collections import defaultdict
from contextlib import contextmanager

# project imports
from bushido.schema.res import UnitLogResponse
from bushido.utils.parsing import (preprocess_input,
                                   parse_datetime_to_timestamp)
from bushido.utils.dt_functions import (get_datetime_from_timestamp,
                                        get_bushido_date_from_datetime)
from bushido.data.conn import SessionFactory
from bushido.data.base_repo import BaseRepository


class Bot:
    def __init__(self, log_services: dict):
        self.sf =  SessionFactory()
        self.log_services = log_services

    @contextmanager
    def get_repo(self):
        with self.sf.get_session() as session:
            repo = BaseRepository(session)
            yield repo

    def get_all_categories(self):
        with self.get_repo() as repo:
            categories = repo.get_all_categories()
            return [dict(key=r.name, value=r.name) for r in categories]

    def get_all_emojis(self):
        with self.get_repo() as repo:
            rows = repo.get_all_emojis()
            return [dict(key=r.unit_name, value=r.emoji) for r in rows]

    def get_emoji_for_unit(self, unit_name):
        with self.get_repo() as repo:
            return repo.get_emoji_for_unit(unit_name)

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        with self.get_repo() as repo:
            units = repo.get_units(unit_name, start_t, end_t)
            dix = defaultdict(list)
            for unit in units:
                bushido_date, hms = self.create_unit_response_dt(unit.timestamp)
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
        bushido_date, hms = self.create_unit_response_dt(timestamp)
        with self.get_repo() as repo:
            unit_name = repo.get_unit_name_for_emoji(emoji)
            category = repo.get_category_for_unit(unit_name)
            log_service = self.log_services[category](repo)
            log_service.process_unit(unit_name, words, timestamp, comment)
        return UnitLogResponse(date=bushido_date,
                               hms=hms,
                               emoji=emoji,
                               unit_name=unit_name,
                               payload=' '.join(words))

    def create_unit_response_dt(self, timestamp):
        dt = get_datetime_from_timestamp(timestamp)
        bushido_date = get_bushido_date_from_datetime(dt)
        hms = dt.strftime('%H%M')
        return bushido_date, hms
