import logging
import sys
from argparse import ArgumentParser
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from rich.logging import RichHandler
from sqlalchemy import Engine
from starlette.middleware.cors import CORSMiddleware

from bushido_server import __version__
from bushido_server.api import router
from bushido_server.conf import DEFAULT_PORT
from bushido_server.persistence import SessionFactory
from bushido_server.persistence.models import Base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


def init_db(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="bushido_server server")
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument("--dev", action="store_true", help="run development server")
    return parser


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    app_.state.sf = SessionFactory()
    yield


def create_app() -> FastAPI:
    app_ = FastAPI(lifespan=lifespan)

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app_.include_router(router)
    return app_


app = create_app()


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        print(f"bushido_server {__version__}")
        sys.exit(0)
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=DEFAULT_PORT,
            log_level="info",
        )


if __name__ == "__main__":
    main()
