import importlib
import importlib.util
import pkgutil

# project imports
from bushido.conf import KEIKO_PROCESSORS


def load_log_service(category: str, package: str = KEIKO_PROCESSORS):
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')

    module_name = f'{package}.{category}'
    module = importlib.import_module(module_name)

    if not hasattr(module, 'LogService'):
        raise ValueError(f'Could not find package {package}')
    cls = getattr(module, 'LogService')
    return cls


def load_log_services(package: str = KEIKO_PROCESSORS):
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')

    log_services = {}
    for finder, category, ispkg in pkgutil.iter_modules(spec.submodule_search_locations):
        module_name = f'{package}.{category}'
        module = importlib.import_module(module_name)

        if hasattr(module, 'UnitService'):
            cls = getattr(module, 'UnitService')
            log_services[category] = cls
    return log_services

