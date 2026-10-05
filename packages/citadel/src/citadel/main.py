import logging
import sys
from argparse import ArgumentParser
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from rich.logging import RichHandler
from starlette.middleware.cors import CORSMiddleware

from citadel import __version__
from citadel.api import health_router, router
from citadel.conf import get_db_url, settings
from citadel.persistence import SessionFactory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


logger = logging.getLogger(__name__)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="citadel server")
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument("--dev", action="store_true", help="run development server")
    return parser


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    logger.info("starting application")
    db_url = get_db_url()
    sf = SessionFactory(db_url=db_url)
    app_.state.sf = sf
    logger.info(
        "database configured: backend=%s database=%s",
        sf.engine.url.get_backend_name(),
        sf.engine.url.database,
    )
    try:
        yield
    finally:
        logger.info("shutting down application")
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
    app_.include_router(health_router)
    return app_


app = create_app()


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        print(f"citadel {__version__}")
        sys.exit(0)
    else:
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            log_level="info",
        )


if __name__ == "__main__":
    main()
