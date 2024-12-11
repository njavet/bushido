from pathlib import Path
import importlib.util
import inspect
from collections import defaultdict
import os

# project imports
from ulib.utils.emojis import create_emoji_dix


class UnitManager:
    def __init__(self, dbm) -> None:
        self.dbm = dbm
        self.emoji2spec: dict = {}
        self.emoji2proc: dict = {}
        # retrievers
        self._load_emojis()
        self._load_processors()

    def process_input(self, unix_timestamp, input_str):
        try:
            emoji, words, comment = self._preprocess_string(input_str)
        except ValueError as err:
            return str(err)
        try:
            emoji_key = self.emoji2spec[emoji].key
            processor = self.emoji2proc[emoji]
        except KeyError:
            return 'Unknown emoji'
        res = processor.process_unit(unix_timestamp, words, comment, emoji_key)
        return res

    def _load_emojis(self):
        emojis = self.dbm.get_emojis()
        # TODO investigate key only vs spec
        self.emoji2spec = create_emoji_dix(emojis)

    def _load_processors(self):
        # TODO refactor
        dix = defaultdict(list)
        self.emoji2proc = {}
        for emoji, spec in self.emoji2spec.items():
            dix[spec.category].append(emoji)

        proc_dir = Path('bushido/procs')
        procs = [file for file in proc_dir.rglob('*.py') if '_' not in file.stem]
        for module_path in procs:
            module_name = module_path.stem
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            proc = [member for member in inspect.getmembers(module)
                    if inspect.isclass(member[1]) and member[0] == 'UnitProcessor'][0][1]
            for emoji in dix[module_name]:
                self.emoji2proc[emoji] = proc(self.dbm.engine)

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
