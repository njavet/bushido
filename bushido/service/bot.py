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

    def get_all_emojis(self):
        with self.get_repo() as repo:
            rows = repo.get_all_emojis()
            return [dict(key=r.unit_name, value=r.emoji) for r in rows]

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        with self.get_repo() as repo:
            units = repo.get_units(unit_name, start_t, end_t)
            dix = defaultdict(list)
            for unit in units:
                dt = get_datetime_from_timestamp(unit.timestamp)
                bushido_dt = get_bushido_date_from_datetime(dt)
                hms = dt.strftime('%H%M')
                dix[bushido_dt].append({'hms': hms,
                                        'emoji': unit.emoji,
                                        'payload': unit.payload})
            return dix

    def log_unit(self, text):
        emoji, words, comment = preprocess_input(text)
        timestamp, words = parse_datetime_to_timestamp(words)
        dt = get_datetime_from_timestamp(timestamp)
        hms = dt.strftime('%H%M')
        bushido_date = get_bushido_date_from_datetime(dt)
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
