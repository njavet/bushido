from pathlib import Path
import importlib
import inspect
import logging

from bushido.exceptions import ProcessingError
from bushido.filters import preprocess_string
from bushido.db import init_database

logger = logging.getLogger(__name__)


class UnitManager:
    def __init__(self) -> None:
        self.umoji2proc: dict = {}
        self.emoji2umoji: dict = {}
        self._load_categories()

    def _load_categories(self):
        categories = Path('keikolib/category')
        # all file_path in categories should be valid category implementations
        db_models = []
        for file_path in categories.rglob('*.py'):
            module_path = str(file_path.with_suffix('')).replace('/', '.')
            module = importlib.import_module(module_path)
            category = module_path.split('.')[2]
            keiko_name = category.capitalize()
            keiko = [member for member in inspect.getmembers(module)
                     if inspect.isclass(member[1]) and member[0] == keiko_name][0][1]
            db_models.append(keiko)
            self._load_processors(category, module)
            self._load_incomplete_emojis(module)
        init_database('test.db', db_models)

    def _load_processors(self, category, module) -> None:
        for umoji, name in module.Umojis.umoji2uname.items():
            self.umoji2proc[umoji] = module.Processor(category, name, umoji)

    def _load_incomplete_emojis(self, module) -> None:
        for emoji, umoji in module.Umojis.emoji2umoji.items():
            self.emoji2umoji[emoji] = umoji

    def log_unit(self,
                 budoka_id: int,
                 timestamp: float,
                 input_string: str) -> str:
        """
        interface for users of the library
        """
        # preprocess input string
        try:
            emoji, words, comment = preprocess_string(input_string)
        except ProcessingError as err:
            return str(err)

        # convert single char emoji to double
        try:
            umoji = self.emoji2umoji[emoji]
        except KeyError:
            umoji = emoji

        # dispatch
        try:
            self.umoji2proc[umoji].process_unit(budoka_id,
                                                timestamp,
                                                words,
                                                comment)
        except KeyError:
            return 'unknown emoji'
        except ProcessingError as err:
            return str(err)
