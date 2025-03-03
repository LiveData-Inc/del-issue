# config.py

from functools import cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_prefix="SA_")

    # Expected to be set from a `.env` file
    drivername: str | None = "sqlite+aiosqlite"
    username: str | None = None
    password: str | None = None
    host: str | None = None
    port: int | None = None
    database: str | None = "./test.db"
    query: dict | None = None
    driver: str | None = None
    odbc_connect: str | None = None
    echo: bool = False

    @computed_field
    @property
    def db_url(self) -> URL:
        """A computed property that builds a SQLAlchemy URL."""
        query = self.query or {}
        if self.odbc_connect:
            query["odbc_connect"] = self.odbc_connect
        if self.driver:
            query["driver"] = self.driver
        return URL.create(
            drivername=self.drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            query=query
        )


@cache
def get_settings() -> Settings:
    return Settings()
