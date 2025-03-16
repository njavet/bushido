from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# project imports
from bushido.web.endpoints import router


def create_fastapi_app():
    app = FastAPI()
    app.mount('/static',
              StaticFiles(directory='static'), name='static')
    app.include_router(router)
    return app
