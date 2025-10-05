import logging
import sys
from argparse import ArgumentParser
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from rich.logging import RichHandler
from starlette.middleware.cors import CORSMiddleware

from bushido import __version__
from bushido.core.conf import DEFAULT_PORT
from bushido.infra.db.conn import SessionFactory
from bushido.web import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="bushido server")
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument("--tui", action="store_true", help="run Textual App ")
    parser.add_argument("--dev", action="store_true", help="run development server")
    return parser


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.sf = SessionFactory()
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        print(f"bushido {__version__}")
        sys.exit(0)

    elif args.tui:
        pass

    elif args.dev:
        uvicorn.run(
            "bushido.main:create_app",
            port=DEFAULT_PORT,
            reload=True,
            factory=True,
            log_level="debug",
        )
    else:
        uvicorn.run(
            "bushido.main:create_app",
            port=DEFAULT_PORT,
            factory=True,
            log_level="info",
        )
