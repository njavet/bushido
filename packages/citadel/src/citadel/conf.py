from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


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
