import logging
import sys
from argparse import ArgumentParser
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from sqlalchemy import URL
from fastapi import FastAPI
from rich.logging import RichHandler
from starlette.middleware.cors import CORSMiddleware

from bushido_server import __version__
from bushido_server.api import router
from bushido_server.conf import DbBackend, Settings, settings
from bushido_server.persistence import SessionFactory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


logger = logging.getLogger(__name__)


def get_db_url(settings: Settings) -> str | URL:
    match settings.db_backend:
        case DbBackend.SQLITE:
            return f"sqlite:///{settings.sqlite_path}"

        case DbBackend.POSTGRES:
            if settings.postgres_url is None:
                raise ValueError("POSTGRES_URL is required")
            return settings.postgres_url

        case DbBackend.AZURE_SQL:
            if (
                settings.azure_sql_host is None
                or settings.azure_sql_database is None
                or settings.azure_sql_user is None
                or settings.azure_sql_password is None
            ):
                raise ValueError("Azure SQL configuration incomplete")

            return URL.create(
                "mssql+pyodbc",
                username=settings.azure_sql_user,
                password=settings.azure_sql_password,
                host=settings.azure_sql_host,
                port=1433,
                database=settings.azure_sql_database,
                query={
                    "driver": "ODBC Driver 18 for SQL Server",
                    "Encrypt": "yes",
                    "TrustServerCertificate": "no",
                },
            )

        case _:
            raise ValueError(f"Unsupported DB backend: {settings.db_backend}")


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="bushido_server server")
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument("--dev", action="store_true", help="run development server")
    return parser


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    logger.info('starting application')
    db_url = get_db_url(settings)
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
