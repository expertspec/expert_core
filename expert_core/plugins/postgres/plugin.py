from __future__ import annotations

from asyncio import current_task, get_event_loop
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any, Callable, AsyncGenerator

import asyncpg
from addict import Dict
from asyncpg import Connection as AsyncConnection
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.requests import HTTPConnection

from expert_core.plugins.base.plugin import Plugin
from expert_core.plugins.postgres.settings import PostgresSettings


class PostgresPlugin(Plugin):
    def __init__(self, app: FastAPI | None = None, config: PostgresSettings | None = None):
        self.config = config or PostgresSettings()

        self.engine: AsyncEngine | None = None
        self.listener: AsyncConnection | None = None
        self.session_factory: async_scoped_session | None = None

        super().__init__(app)

    def init(self):
        self.engine = create_async_engine(url=self.config.url, **self.config.opts)
        self.session_factory = async_scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )

    async def on_startup(self):
        self.listener = await asyncpg.connect(
            self.config.url.replace("+asyncpg", ""),
            loop=get_event_loop(),
            **self.config.opts,
        )

    async def on_shutdown(self):
        await self.session_factory.close_all()
        await self.session_factory.remove()
        await self.engine.dispose()
        await self.listener.close()

    async def ping(self):
        async with self.engine.begin() as connection:
            return (await connection.execute(text("SELECT 1;"))).one() == (1,)

    async def ping_listener(self) -> bool:
        return not self.listener.is_closed()

    async def health(self) -> dict[str, Any]:
        return {
            "url": self.config.url,
            "pong": await self.ping(),
            "listener-pong": await self.ping_listener(),
        }

    async def add_listener(self, channel: str, handler: Callable) -> None:
        await self.listener.add_listener(channel, handler)

    async def remove_listener(self, channel: str, handler: Callable) -> None:
        await self.listener.remove_listener(channel, handler)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AbstractAsyncContextManager[AsyncSession]]:
        session: AsyncSession = self.session_factory()

        try:
            yield session
        except Exception as e:
            await session.rollback()

            raise e
        finally:
            await session.close()


Postgres = PostgresPlugin
Database = Postgres


async def init_psql(app: FastAPI | Any, config: PostgresSettings | None = None):
    if not hasattr(app.state, "plugins"):
        app.state.plugins = Dict()
    app.state.plugins.psql = PostgresPlugin(app, config)

    await app.state.plugins.psql.on_startup()


async def depends_db(connection: HTTPConnection) -> Database:
    if not hasattr(connection.app.state, "plugins") or not hasattr(connection.app.state.plugins, "psql"):
        raise Exception("Database is not initialized")

    return connection.app.state.plugins.psql


depends_psql = depends_db


async def depends_db_engine(connection: HTTPConnection) -> AsyncEngine:
    if not hasattr(connection.app.state, "plugins") or not hasattr(connection.app.state.plugins, "psql"):
        raise Exception("Database is not initialized")

    return connection.app.state.plugins.psql.engine


depends_psql_engine = depends_db_engine


async def depends_db_session_factory(connection: HTTPConnection) -> async_scoped_session:
    if not hasattr(connection.app.state, "plugins") or not hasattr(connection.app.state.plugins, "psql"):
        raise Exception("Database is not initialized")

    return connection.app.state.plugins.psql.session_factory


depends_psql_session_factory = depends_db_session_factory


async def depends_db_listener(connection: HTTPConnection) -> AsyncConnection:
    if not hasattr(connection.app.state, "plugins") or not hasattr(connection.app.state.plugins, "psql"):
        raise Exception("Database is not initialized")

    return connection.app.state.plugins.psql.listener


depends_psql_listener = depends_db_listener
