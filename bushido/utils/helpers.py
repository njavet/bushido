import importlib
import importlib.util
import pkgutil
from bushido.conf import KEIKO_PROCESSORS


def load_unit_services(package: str = KEIKO_PROCESSORS):
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')

    unit_services = {}
    for finder, category, ispkg in pkgutil.iter_modules(spec.submodule_search_locations):
        module_name = f'{package}.{category}'
        module = importlib.import_module(module_name)

        if hasattr(module, 'UnitService'):
            cls = getattr(module, 'UnitService')
            unit_services[category] = cls
    return unit_services

