from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# project imports
from bushido.conf import DEFAULT_PORT
from bushido.service.setup import setup_dm, setup_up
from bushido.web import router


def create_app():
    app = FastAPI()

    app.mount('/bushido/static',
              StaticFiles(directory='bushido/static'), name='static')
    app.state.dm = setup_dm()
    app.state.up = setup_up(app.state.dm)
    app.add_middleware(CORSMiddleware,
                       allow_origins=['http://localhost:5173'],
                       allow_methods=["*"],
                       allow_headers=["*"],)

    app.include_router(router)

    return app


def run_app():
    uvicorn.run('bushido.main:create_app',
                port=DEFAULT_PORT,
                reload=True,
                factory=True,
                log_level='debug')


if __name__ == '__main__':
    run_app()
