from __future__ import annotations

from typing import Any

from addict import Dict
from fastapi import FastAPI
from redis import asyncio as aioredis
from starlette.requests import HTTPConnection

from avatar_core.plugins.base.plugin import Plugin
from avatar_core.plugins.redis.settings import RedisSettings


class RedisPlugin(Plugin):
    def __init__(self, app: FastAPI | None = None, config: RedisSettings | None = None):
        self.config = config or RedisSettings()

        self.redis: aioredis.Redis | None = None

        super().__init__(app)

    def init(self):
        self.redis = aioredis.from_url(url=self.config.url, **self.config.opts)

    async def on_shutdown(self):
        self.redis = None

    async def ping(self) -> bool:
        return await self.redis.ping()

    async def health(self) -> dict[str, Any]:
        return {
            "url": self.config.url,
            "pong": await self.redis.ping(),
        }


Redis = RedisPlugin


async def init_redis(app: FastAPI, config: RedisSettings = None):
    if not hasattr(app.state, "plugins"):
        app.state.plugins = Dict()
    app.state.plugins.redis = RedisPlugin(app, config)


async def depends_redis(connection: HTTPConnection) -> aioredis.Redis:
    if not hasattr(connection.app.state, "plugins") or not hasattr(connection.app.state.plugins, "redis"):
        raise Exception("Redis is not initialized")

    return connection.app.state.plugins.redis
