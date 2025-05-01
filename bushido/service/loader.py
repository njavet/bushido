import importlib
import importlib.util
import pkgutil

# project imports
from bushido.conf import ORM_MODELS, KEIKO_PROCESSORS


def load_orm_models(package: str = ORM_MODELS):
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')
    for finder, category, ispkg in pkgutil.iter_modules(spec.submodule_search_locations):
        module_name = f'{package}.{category}'
        module = importlib.import_module(module_name)


def load_log_service(category: str, package: str = KEIKO_PROCESSORS):
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')

    module_name = f'{package}.{category}'
    module = importlib.import_module(module_name)

    if not hasattr(module, 'create_keiko'):
        raise ValueError(f'Could not find package {package}')
    fn = getattr(module, 'create_keiko')
    return fn


def load_all_log_services(package: str = KEIKO_PROCESSORS):
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')

    log_services = {}
    for finder, category, ispkg in pkgutil.iter_modules(spec.submodule_search_locations):
        module_name = f'{package}.{category}'
        module = importlib.import_module(module_name)

        if hasattr(module, 'create_keiko'):
            fn = getattr(module, 'create_keiko')
            log_services[category] = fn
    return log_services
