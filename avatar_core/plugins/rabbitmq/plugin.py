from __future__ import annotations

from asyncio import get_event_loop
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any, Callable

from addict import Dict
from aio_pika import connect_robust
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from aio_pika.pool import Pool
from fastapi import FastAPI
from starlette.requests import HTTPConnection

from avatar_core.plugins.base.plugin import Plugin
from avatar_core.plugins.rabbitmq.settings import RabbitMQSettings


class RabbitMQPlugin(Plugin):
    def __init__(self, app: FastAPI | None = None, config: RabbitMQSettings | None = None):
        self.config = config or RabbitMQSettings()

        self.connection_pool: Pool | None = None
        self.channel_pool: Pool | None = None

        super().__init__(app)

    def init(self):
        self.connection_pool = Pool(self._connection, loop=get_event_loop(), **self.config.pool_opts)
        self.channel_pool = Pool(self._channel, loop=get_event_loop(), **self.config.pool_opts)

    async def on_shutdown(self):
        await self._connection.close()
        await self._channel.close()

    async def _connection(self) -> AbstractRobustConnection:
        return await connect_robust(url=self.config.url, loop=get_event_loop(), **self.config.connection_opts)

    async def _channel(self) -> AbstractChannel:
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    @asynccontextmanager
    async def channel(self) -> Callable[..., AbstractAsyncContextManager[AbstractChannel]]:
        async with self.channel_pool.acquire() as channel:
            yield channel

    async def ping(self) -> bool:
        return not self._connection.is_closed

    async def health(self) -> dict[str, Any]:
        return {
            "url": self.config.url,
            "pong": await self.ping(),
        }


RabbitMQ = RabbitMQPlugin


async def init_rabbitmq(app: FastAPI, config: RabbitMQSettings = None):
    config = config or RabbitMQSettings()
    if not hasattr(app.state, "plugins"):
        app.state.plugins = Dict()

    app.state.plugins.rabbitmq = RabbitMQPlugin(app, config)


async def depends_rabbitmq(connection: HTTPConnection) -> RabbitMQ:
    if not hasattr(connection.app.state, "plugins") or not hasattr(connection.app.state.plugins, "rabbitmq"):
        raise Exception("RabbitMQ is not initialized")

    return connection.app.state.rabbitmq
