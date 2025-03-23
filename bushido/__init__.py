import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_fastapi_app():
    app = FastAPI()
    app.mount('/static',
              StaticFiles(directory='static'), name='static')
    # project imports
    from bushido.web.base import router
    app.include_router(router)
    return app


def run_app():
    uvicorn.run('bushido:create_fastapi_app',
                port=8080,
                reload=True,
                factory=True,
                log_level='debug')
