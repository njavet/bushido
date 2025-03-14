from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from unitlib.unitlib import UnitManager

# project imports
from bushido.api.endpoints import router


def create_fastapi_app():
    um = UnitManager('sqlite:///bushido.db')
    app = FastAPI()
    app.mount('/bushido/static',
              StaticFiles(directory='bushido/static'), name='static')
    app.include_router(router)
    return app
