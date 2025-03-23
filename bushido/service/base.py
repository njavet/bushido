from collections import defaultdict
from pathlib import Path
import importlib

# project imports
from bushido.data.base import DatabaseManager
from bushido.service.categories.category import InputProcessor


class BaseService:
    def __init__(self):
        self.dbm = DatabaseManager(db_url='sqlite:///bushido.db')
        self.emoji_specs = self.dbm.load_emojis()
        self.iproc = InputProcessor(self.load_processors())

    def construct_autocomplete_dix(self):
        dix = {}
        for emoji_spec in self.emoji_specs:
            dix[emoji_spec.unit_name] = emoji_spec.emoji
        return dix

    def construct_processor_dix(self):
        dix = defaultdict(list)
        for emoji_spec in self.emoji_specs:
            dix[emoji_spec.category_name].append(emoji_spec)
        return dix

    def load_processors(self):
        emoji2processor = {}
        categories = Path('bushido', 'service', 'categories')

        for category_name, es_lst in self.construct_processor_dix().items():
            module_path = categories / category_name
            try:
                module = importlib.import_module('.'.join(module_path.parts))
            except ModuleNotFoundError:
                print(f'{category_name} is not ready')
            else:
                unit_processor = module.UnitProcessor(self.dbm.engine)
                for emoji_spec in es_lst:
                    emoji2processor[emoji_spec.emoji] = unit_processor
                    emoji2processor[emoji_spec.emoji_text] = unit_processor
        return emoji2processor

