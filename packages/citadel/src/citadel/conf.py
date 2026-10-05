from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DbBackend(StrEnum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"
    AZURE_SQL = "azure_sql"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
    )

    host: str = "0.0.0.0"
    port: int = 8000

    db_backend: DbBackend = DbBackend.POSTGRES

    # SQLite
    sqlite_path: str | None = None

    # PostgreSQL
    postgres_host: str | None = None
    postgres_port: int = 5432
    postgres_database: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None

    # Azure SQL
    azure_sql_host: str | None = None
    azure_sql_database: str | None = None
    azure_sql_user: str | None = None
    azure_sql_password: str | None = None


settings = Settings()


def get_db_url() -> URL | str:
    match settings.db_backend:
        case DbBackend.SQLITE:
            return f"sqlite:///{settings.sqlite_path}"

        case DbBackend.POSTGRES:
            if (
                settings.postgres_host is None
                or settings.postgres_database is None
                or settings.postgres_user is None
                or settings.postgres_password is None
            ):
                raise ValueError("POSTGRES config is required")
            return URL.create(
                "postgresql+psycopg",
                username=settings.postgres_user,
                password=settings.postgres_password,
                host=settings.postgres_host,
                port=settings.postgres_port,
                database=settings.postgres_database,
            )

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
