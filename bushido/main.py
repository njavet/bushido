from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from bushido.conf import DEFAULT_PORT
from bushido.data.conn import SessionFactory
from bushido.web.api import router


def create_app():
    app = FastAPI()

    app.add_middleware(CORSMiddleware,
                       allow_origins=['http://localhost:5173'],
                       allow_methods=["*"],
                       allow_headers=["*"],)
    app.include_router(router)
    app.state.sf = SessionFactory()

    return app


def run_app():
    uvicorn.run('bushido.main:create_app',
                port=DEFAULT_PORT,
                reload=True,
                factory=True,
                log_level='debug')


if __name__ == '__main__':
    run_app()
