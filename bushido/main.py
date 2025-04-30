from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# project imports
from bushido.conf import DEFAULT_PORT
from bushido.service.bot import Bot
from bushido.web import router


def create_app():
    app = FastAPI()

    app.add_middleware(CORSMiddleware,
                       allow_origins=['http://localhost:5173'],
                       allow_methods=["*"],
                       allow_headers=["*"],)
    app.include_router(router)
    app.state.bot = Bot()

    return app


def run_app():
    uvicorn.run('bushido.main:create_app',
                port=DEFAULT_PORT,
                reload=True,
                factory=True,
                log_level='debug')


if __name__ == '__main__':
    run_app()
