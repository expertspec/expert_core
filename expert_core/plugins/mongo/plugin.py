from __future__ import annotations

from typing import Any

from addict import Dict
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import HTTPConnection

from expert_core.plugins.base.plugin import Plugin
from expert_core.plugins.mongo.settings import MongoSettings


class MongoPlugin(Plugin):
    def __init__(self, app: FastAPI | None = None, config: MongoSettings | None = None):
        self.config = config or MongoSettings()

        self.client: AsyncIOMotorClient | None = None

        super().__init__(app)

    def init(self):
        self.client = AsyncIOMotorClient(self.config.url, **self.config.opts)

    async def on_shutdown(self):
        self.client.close()

    async def ping(self) -> bool:
        return await self.client.conn.command({"dbStats": 1})

    async def health(self) -> dict[str, Any]:
        return {
            "url": self.config.url,
            "pong": await self.ping(),
        }


async def init_mongo(app: FastAPI, config: MongoSettings = None):
    config = config or MongoSettings()
    if not hasattr(app.state, "plugins"):
        app.state.plugins = Dict()
    app.state.plugins.mongo = MongoPlugin(app, config)

    await app.state.plugins.mongo.startup()


Mongo = MongoPlugin


async def depends_mongo(connection: HTTPConnection) -> Mongo:
    return connection.app.state.plugins.mongo


async def depends_mongo_client(connection: HTTPConnection) -> AsyncIOMotorClient:
    return connection.app.state.plugins.mongo.client
