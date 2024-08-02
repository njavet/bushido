import importlib.util
import inspect
from pathlib import Path

# project imports
from .manager import UnitManager
from .db import init_database


def get_category_path():
    current_dir = Path(__file__).resolve().parent
    target_directory = current_dir / 'category'
    return target_directory


def load_categories(unit_manager: UnitManager):
    categories = get_category_path()
    # all file_path in categories should be valid category implementations
    db_models = []
    for module_path in categories.rglob('*.py'):
        module_name = module_path.stem
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        keiko_name = module_name.capitalize()
        keiko = [member for member in inspect.getmembers(module)
                 if inspect.isclass(member[1]) and member[0] == keiko_name][0][1]
        db_models.append(keiko)

        unit_manager.load_classes(module_name, module)
        unit_manager.load_incomplete_emojis(module)
    init_database('test.db', db_models)


um = UnitManager()
load_categories(um)

