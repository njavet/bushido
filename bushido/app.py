from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# project imports
from bushido.api.endpoints import router


def create_fastapi_app():
    app = FastAPI()
    app.mount('/bushido/static',
              StaticFiles(directory='bushido/static'), name='static')
    app.include_router(router)
    return app
