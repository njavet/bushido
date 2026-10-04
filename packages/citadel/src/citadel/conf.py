from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DbBackend(StrEnum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"
    AZURE_SQL = "azure_sql"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "0.0.0.0"
    port: int = 8000

    db_backend: DbBackend = DbBackend.POSTGRES

    # SQLite
    sqlite_path: str | None = None

    # PostgreSQL
    postgres_url: str | None = None

    # Azure SQL
    azure_sql_host: str | None = None
    azure_sql_database: str | None = None
    azure_sql_user: str | None = None
    azure_sql_password: str | None = None


settings = Settings()


def get_db_url() -> str | URL:
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
