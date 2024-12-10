from pathlib import Path
import importlib.util
import inspect
import os

# project imports
from bushido.utils.emojis import format_emojis

class UnitManager:
    def __init__(self, dbm) -> None:
        self.dbm = dbm
        self.emoji2key: dict = {}
        self.emoji2proc: dict = {}
        # retrievers
        self._load_emojis()
        self._load_processors()

    def _load_emojis(self):
        emojis = self.dbm.get_emojis()

    def _load_processors(self):
        proc_dir = Path('bushido/keikolib')
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


    def _load_processors(self, category, module) -> None:
        for umoji, uname in module.Umojis.umoji2uname.items():
            self.umoji2proc[umoji] = module.Processor(category, uname, umoji)

    def _load_incomplete_emojis(self, module) -> None:
        try:
            for emoji, umoji in module.Umojis.emoji2umoji.items():
                self.emoji2umoji[emoji] = umoji
        except AttributeError:
            pass

    def process_input(self, unix_timestamp, input_str):
        try:
            emoji, words, comment = self._preprocess_string(input_str)
        except ValueError as err:
            return str(err)
        try:
            emoji_key = self.emoji2key[emoji]
            processor = self.emoji2proc[emoji]
        except KeyError:
            return 'Unknown emoji'
        res = processor.process_unit(unix_timestamp, words, comment, emoji_key)
        return res

    @staticmethod
    def _preprocess_string(input_str: str):
        parts = input_str.split('//', 1)
        emoji_payload = parts[0]
        if not emoji_payload:
            raise ValueError('Empty payload')
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        all_words = emoji_payload.split()
        emoji = all_words[0]
        words = all_words[1:]
        return emoji, words, comment
