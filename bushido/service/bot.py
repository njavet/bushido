from contextlib import contextmanager

# project imports
from bushido.schema.res import UnitLogResponse
from bushido.utils.dt_functions import create_unit_response_dt
from bushido.utils.parsing import (preprocess_input,
                                   parse_datetime_to_timestamp)
from bushido.data.conn import SessionFactory
from bushido.data.repo import Repository


class Bot:
    def __init__(self):
        self.sf =  SessionFactory()
        self.unit_services = unit_services

    @contextmanager
    def get_repo(self):
        with self.sf.get_session() as session:
            repo = Repository(session)
            yield repo

    def log_unit(self, text):
        emoji, words, comment = preprocess_input(text)
        timestamp, words = parse_datetime_to_timestamp(words)
        bushido_date, hms = create_unit_response_dt(timestamp)
        with self.get_repo() as repo:
            unit_name = repo.get_unit_name_for_emoji(emoji)
            category = repo.get_category_for_unit(unit_name)
            unit_service = self.unit_services[category](repo)
            unit_service.process_unit(unit_name, words, timestamp, comment)
        return UnitLogResponse(date=bushido_date,
                               hms=hms,
                               emoji=emoji,
                               unit_name=unit_name,
                               payload=' '.join(words))
