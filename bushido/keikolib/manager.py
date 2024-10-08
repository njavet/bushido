import logging
from pathlib import Path
import importlib.util
import inspect
import peewee as pw
import os

from bushido.keikolib.filters import preprocess_string
from bushido.keikolib.db import Unit, Message, init_database, unit_logged


logger = logging.getLogger(__name__)


class UnitManager:
    def __init__(self) -> None:
        # categories
        self.categories: dict = {}
        self.unit_logged = unit_logged
        # needed because of different encoding of emojis (single vs double)
        self.emoji2umoji: dict = {}
        # unit log processors
        self.umoji2proc: dict = {}
        # retrievers
        self._load_categories()

    def _load_categories(self):
        categories = Path('bushido/keikolib')
        # all file_path in categories should be valid category implementations
        db_models = []
        for module_path in categories.rglob('cat_*.py'):
            module_name = module_path.stem[4:]
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            keiko_name = module_name.capitalize()
            keiko = [member for member in inspect.getmembers(module)
                     if inspect.isclass(member[1]) and member[0] == keiko_name][0][1]
            db_models.append(keiko)

            self.categories[module_name] = module.Category(module_name)
            self._load_processors(module_name, module)
            self._load_incomplete_emojis(module)

        data_dir = os.path.join(os.path.expanduser('~'), '.local/share/bushido')
        db_url = os.path.join(data_dir, 'keiko.db')
        init_database(db_url, db_models)

    def _load_processors(self, category, module) -> None:
        for umoji, uname in module.Umojis.umoji2uname.items():
            self.umoji2proc[umoji] = module.Processor(category, uname, umoji)

    def _load_incomplete_emojis(self, module) -> None:
        try:
            for emoji, umoji in module.Umojis.emoji2umoji.items():
                self.emoji2umoji[emoji] = umoji
        except AttributeError:
            pass

    def log_unit(self,
                 unix_timestamp: float,
                 input_string: str) -> str:
        """
        interface for users of the library
        """
        # preprocess input string
        try:
            emoji, words, comment = preprocess_string(input_string)
        except ValueError as err:
            return str(err)

        # convert single char emoji to double
        try:
            umoji = self.emoji2umoji[emoji]
        except KeyError:
            umoji = emoji

        # dispatch
        try:
            self.umoji2proc[umoji].process_unit(unix_timestamp,
                                                words,
                                                comment)
        except KeyError:
            return 'unknown emoji'
        except ValueError as err:
            return str(err)
        else:
            return 'Unit confirmed!'

    @staticmethod
    def retrieve_unit_messages() -> list:
        query = (Message
                 .select()
                 .join(Unit)
                 .order_by(Unit.unix_timestamp))
        return query

    @staticmethod
    def get_last_unit_timestamp():
        query = (Unit
                 .select()
                 .order_by(Unit.unix_timestamp.desc()))
        try:
            unix_timestamp = query.get().unix_timestamp
        except pw.DoesNotExist:
            unix_timestamp = 0

        return unix_timestamp
