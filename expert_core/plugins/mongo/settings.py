from __future__ import annotations

from pydantic import BaseSettings


class MongoSettings(BaseSettings):
    protocol: str = "mongodb"
    host: str = "localhost"
    port: int = 27017

    username: str | None = None
    password: str | None = None

    class Config:
        env_prefix: str = "mongo_"
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
        }
