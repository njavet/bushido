from pathlib import Path
import importlib
import importlib.util

# project imports
from bushido.conf import DB_URL, KEIKO_PROCESSORS
from bushido.data.manager import DataManager
from bushido.service.units import UnitProcessor


def setup_dm():
    dm = DataManager(db_url=DB_URL)
    return dm


def setup_up(dm):
    up = UnitProcessor(dm)
    return up


def load_keiko_processors_from_package(package: str = KEIKO_PROCESSORS) -> dict:
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')

    package_path = Path(spec.submodule_search_locations[0])
    processors = {}

    for file in package_path.glob('*.py'):
        if file.name.startswith('_'):
            continue

        category_name = file.stem
        module_name = f'{package}.{file.stem}'
        module = importlib.import_module(module_name)

        if not hasattr(module, 'KeikoProcessor'):
            raise ImportError(f'{module_name} does not define KeikoProcessor')

        cls = getattr(module, 'KeikoProcessor')
        processors[category_name] = cls()

    return processors
