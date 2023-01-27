from __future__ import annotations

from pydantic import BaseSettings


class RabbitMQSettings(BaseSettings):
    protocol: str = "amqp"
    host: str = "localhost"
    port: int = 5672

    username: str = "guest"
    password: str = "guest"
    virtualhost: str = "/"

    max_size: int | None = 4

    class Config:
        env_prefix: str = "rabbitmq_"
        env_file: str = ".env"
        allow_mutation: bool = False

    @property
    def url(self):
        return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}/{self.virtualhost}"

    @property
    def pool_opts(self):
        return {"max_size": self.max_size}

    @property
    def connection_opts(self):
        return {
            "login": self.username,
            "password": self.password,
        }
