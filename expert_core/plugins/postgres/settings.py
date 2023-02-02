from __future__ import annotations

from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    protocol: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: int = 5432

    user: str = "guest"
    password: str = "guest"

    db: str = "db"

    pool_minsize: int | None = 1
    pool_maxsize: int | None = None

    max_connections: int | None = None
    decode_responses: bool = True

    ttl: int = 3600

    class Config:
        env_prefix: str = "postgres_"
        env_file: str = ".env"
        allow_mutation: bool = False

    @property
    def url(self):
        _url = f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

        return _url

    @property
    def opts(self):
        return {}
