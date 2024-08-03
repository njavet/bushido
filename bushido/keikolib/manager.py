import logging
from pathlib import Path
import importlib.util
import inspect

from bushido.keikolib.filters import preprocess_string
from bushido.keikolib.db import Unit, Message, init_database

logger = logging.getLogger(__name__)


class UnitManager:
    def __init__(self) -> None:
        # needed because of different encoding of emojis (single vs double)
        self.emoji2umoji: dict = {}
        # unit log processors
        self.umoji2proc: dict = {}
        # retrievers
        self.umoji2ret: dict = {}
        self.uname2ret: dict = {}
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

            self._load_classes(module_name, module)
            self._load_incomplete_emojis(module)
        init_database('test.db', db_models)

    def _load_classes(self, category, module) -> None:
        for umoji, uname in module.Umojis.umoji2uname.items():
            self.umoji2proc[umoji] = module.Processor(category, uname, umoji)
            ret = module.Retriever(category, uname)
            self.umoji2ret[umoji] = ret
            self.uname2ret[uname] = ret

    def _load_incomplete_emojis(self, module) -> None:
        try:
            for emoji, umoji in module.Umojis.emoji2umoji.items():
                self.emoji2umoji[emoji] = umoji
        except AttributeError:
            pass

    def log_unit(self,
                 timestamp: float,
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
            self.umoji2proc[umoji].process_unit(timestamp,
                                                words,
                                                comment)
        except KeyError:
            return 'unknown emoji'
        except ValueError as err:
            return str(err)

    def retrieve_units(self, uname=None) -> list:
        pass

    @staticmethod
    def retrieve_messages() -> list:
        query = (Unit
                 .select(Unit, Message)
                 .join(Message)
                 .order_by(Unit.timestamp.desc()))
        return query
