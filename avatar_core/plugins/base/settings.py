from __future__ import annotations

from pydantic.env_settings import BaseSettings


class RedisSettings(BaseSettings):
    protocol: str = "redis"
    host: str = "localhost"
    port: int = 6379

    user: str | None = None
    password: str | None = None

    db: int | None = None

    pool_minsize: int | None = 1
    pool_maxsize: int | None = None

    max_connections: int | None = None
    decode_responses: bool = True

    ttl: int = 3600

    class Config:
        env_prefix: str = "redis_"
        env_file: str = ".env"
        allow_mutation: bool = False

    @property
    def url(self):
        _url = f"{self.protocol}://{self.host}:{self.port}"

        if self.db is not None:
            _url = f"{_url}/{self.db}"

        return _url

    @property
    def opts(self):
        return {
            "db": self.db,
            "username": self.username,
            "password": self.password,
            "max_connections": self.max_connections,
            "decode_responses": self.decode_responses,
        }
