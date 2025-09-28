import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich.logging import RichHandler
from starlette.middleware.cors import CORSMiddleware

from bushido.infra.db.conn import SessionFactory
from bushido.web import router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.sf = SessionFactory()
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:5173'],
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.include_router(router)
    return app
