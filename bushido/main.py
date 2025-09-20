import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich.logging import RichHandler
from starlette.middleware.cors import CORSMiddleware

# project imports
from bushido.core.app_context import app_context
from bushido.db.conn import SessionFactory
from bushido.web import router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    dbs = {"sqlite": SessionFactory("sqlite")}
    app_context.dbs = dbs
    yield
    app_context.dbs = None


def create_app():
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app
