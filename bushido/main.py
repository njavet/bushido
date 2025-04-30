import importlib
import importlib.util
import pkgutil
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# project imports
from bushido.conf import DEFAULT_PORT, KEIKO_PROCESSORS
from bushido.service.bot import Bot
from bushido.web import router


def load_log_services(package: str = KEIKO_PROCESSORS):
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')

    log_services = {}
    for finder, category, ispkg in pkgutil.iter_modules(spec.submodule_search_locations):
        module_name = f'{package}.{category}'
        module = importlib.import_module(module_name)

        if hasattr(module, 'LogService'):
            cls = getattr(module, 'LogService')
            log_services[category] = cls
    return log_services


def create_app():
    app = FastAPI()

    app.add_middleware(CORSMiddleware,
                       allow_origins=['http://localhost:5173'],
                       allow_methods=["*"],
                       allow_headers=["*"],)
    app.include_router(router)
    log_services = load_log_services()
    app.state.bot = Bot(log_services=log_services)

    return app


def run_app():
    uvicorn.run('bushido.main:create_app',
                port=DEFAULT_PORT,
                reload=True,
                factory=True,
                log_level='debug')


if __name__ == '__main__':
    run_app()
