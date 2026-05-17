import logging
import sys
from argparse import ArgumentParser
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from rich.logging import RichHandler
from sqlalchemy import Engine
from starlette.middleware.cors import CORSMiddleware

from bushido import __version__
from bushido.application.registry import build_registry
from bushido.application.service import LogUnitService
from bushido.application.service.load_unit_service import LoadUnitService
from bushido.conf import DEFAULT_PORT
from bushido.interfaces.tui.tui import BushidoApp
from bushido.interfaces.web import router
from bushido.persistence._sf import SessionFactory
from bushido.persistence.models import Base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


def init_db(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="bushido server")
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument(
        "--tui", action="store_true", default=True, help="run Textual App "
    )
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
        sf = SessionFactory()
        init_db(engine=sf.engine)
        registry = build_registry()
        log_unit_service = LogUnitService(registry=registry)
        load_unit_service = LoadUnitService(registry=registry)
        BushidoApp(sf, log_unit_service, load_unit_service).run()
    else:
        uvicorn.run(
            "bushido.web.web:create_app",
            port=DEFAULT_PORT,
            factory=True,
            log_level="info",
        )


if __name__ == "__main__":
    main()
