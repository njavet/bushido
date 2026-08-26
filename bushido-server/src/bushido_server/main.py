import logging
import os
import sys
from argparse import ArgumentParser
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from rich.logging import RichHandler
from starlette.middleware.cors import CORSMiddleware

from bushido_server import __version__
from bushido_server.api import router
from bushido_server.persistence import SessionFactory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)

# TODO refactor
load_dotenv()
PORT = int(os.environ.get("DEFAULT_PORT", "8000"))
DB_URL = os.environ.get("BUSHIDO_DB_URL", "sqlite:///bushido.db")


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="bushido_server server")
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument("--dev", action="store_true", help="run development server")
    return parser


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    sf = SessionFactory(db_url=DB_URL)
    app_.state.sf = sf
    try:
        yield
    finally:
        sf.engine.dispose()


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
            port=PORT,
            log_level="info",
        )


if __name__ == "__main__":
    main()
