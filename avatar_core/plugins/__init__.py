from fastapi_keycloak.api import FastAPIKeycloak
from starlette.requests import HTTPConnection

from avatar_core.plugins.keycloak import Keycloak, KeycloakPlugin
from avatar_core.plugins.keycloak import depends_idp as keycloak_depends_idp
from avatar_core.plugins.keycloak import depends_keycloak, init_keycloak
from avatar_core.plugins.mongo import Mongo, MongoPlugin, MongoSettings, depends_mongo, depends_mongo_client, init_mongo
from avatar_core.plugins.postgres import Postgres, PostgresPlugin, PostgresSettings
from avatar_core.plugins.postgres import depends_db as psql_depends_db
from avatar_core.plugins.postgres import depends_db_engine, depends_db_session_factory, init_psql
from avatar_core.plugins.rabbitmq import depends_rabbitmq, init_rabbitmq
from avatar_core.plugins.redis import depends_redis, init_redis


async def depends_idp(connection: HTTPConnection) -> FastAPIKeycloak:
    if hasattr(connection.app.state, "plugins"):
        if hasattr(connection.app.state.plugins, "keycloak"):
            return await keycloak_depends_idp(connection)

    raise Exception("IDP plugin is not initialized")


async def depends_db(connection: HTTPConnection) -> Postgres:
    if hasattr(connection.app.state, "plugins"):
        if hasattr(connection.app.state.plugins, "psql"):
            return await psql_depends_db(connection)

    raise Exception("Database plugin is not initialized")


__all__ = [
    "init_keycloak",
    "init_redis",
    "init_mongo",
    "init_rabbitmq",
    "depends_rabbitmq",
    "init_psql",
    "depends_keycloak",
    "depends_idp",
    "Keycloak",
    "KeycloakPlugin",
    "Mongo",
    "MongoPlugin",
    "MongoSettings",
    "depends_mongo",
    "depends_mongo_client",
    "depends_db",
    "init_psql",
    "Postgres",
    "PostgresPlugin",
    "PostgresSettings",
    "depends_psql",
    "depends_db_engine",
    "depends_db_session_factory",
    "depends_redis",
]
