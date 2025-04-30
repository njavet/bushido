import importlib
import importlib.util
from collections import defaultdict
from contextlib import contextmanager

# project imports
from bushido.conf import KEIKO_PROCESSORS
from bushido.utils.parsing import preprocess_input
from bushido.utils.dt_functions import (get_datetime_from_timestamp,
                                        get_bushido_date_from_datetime)
from bushido.data.conn import SessionFactory
from bushido.data.base_repo import BaseRepository


class Bot:
    def __init__(self):
        self.sf =  SessionFactory()

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
                hms = dt.strftime('%H:%M')
                dix[bushido_dt].append({'hms': hms,
                                        'emoji': unit.emoji,
                                        'payload': unit.payload})
            return dix

    def log_unit(self, text):
        emoji, words, comment = preprocess_input(text)
        with self.get_repo() as repo:
            unit_name = repo.get_unit_name_for_emoji(emoji)
            category = repo.get_category_for_unit(unit_name)
            log_service = self.load_log_service(category)(repo)
            log_service.process_unit(unit_name, words, comment)

    @staticmethod
    def load_log_service(category: str, package: str = KEIKO_PROCESSORS):
        spec = importlib.util.find_spec(package)
        if spec is None or not spec.submodule_search_locations:
            raise ImportError(f'Could not find package {package}')

        # package_path = Path(spec.submodule_search_locations[0])
        module_name = f'{package}.{category}'
        module = importlib.import_module(module_name)

        if not hasattr(module, 'LogService'):
            raise ImportError(f'{module_name} does not define LogService')

        cls = getattr(module, 'LogService')
        return cls
