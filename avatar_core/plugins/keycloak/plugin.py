from __future__ import annotations

import json

import re
from typing import Any

from addict import Dict
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.params import Security
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi_keycloak import FastAPIKeycloak
from fastapi_keycloak.model import KeycloakToken, KeycloakUser, OIDCUser
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from starlette.requests import Request

from avatar_core.plugins.base.plugin import Plugin
from avatar_core.plugins.keycloak.settings import KeycloakSettings


class KeycloakPlugin(Plugin):
    def __init__(self, *, app: FastAPI | None = None, config: KeycloakSettings | None = None):

        self.config = config or KeycloakSettings()
        self.idp: FastAPIKeycloak | None = None

        super().__init__(app)
        if app is not None:
            self.idp.add_swagger_config(app)

        self.current_user = self.idp.get_current_user()

    def init(self):
        self.idp = FastAPIKeycloak(
            server_url=self.config.url,
            callback_uri=self.config.callback_uri,
            **self.config.opts,
        )

    async def ping(self) -> bool:
        return True

    async def health(self) -> dict[str, Any]:
        return {
            "server_url": self.config.url,
            "callback_uri": self.config.callback_uri,
            "pong": await self.ping(),
        }

    async def create_user(
        self,
        username: str,
        password: str,
        email: str,
        first_name: str,
        last_name: str,
        enabled: bool = True,
        initial_roles: list[str] | None = None,
        send_email_verification: bool = True,
        attributes: dict[str, Any] | None = None,
    ) -> KeycloakUser:
        return await self.idp.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            enabled=enabled,
            initial_roles=initial_roles,
            send_email_verification=send_email_verification,
            attributes=attributes,
        )

    async def user_login(self, username: str, password: str) -> KeycloakToken:
        return await self.idp.user_login(username=username, password=password)

    async def update_permissions(self, user: OIDCUser | str, *item_ids: str, permissions: str | None = None):
        if len(item_ids) == 0:
            return

        user_id = user.sub if isinstance(user, OIDCUser) else user
        keycloak_user = self.idp.get_user(user_id=user_id)
        _attributes = keycloak_user.attributes or {}

        item_id = ""
        if len(item_ids) == 1:
            item_id = item_ids[0]
        else:
            for _item_id in item_ids:
                item_id = f"{item_id}{_item_id}:"
            item_id = item_id[:-1]
        _attributes.pop(item_id, None)

        if permissions is not None:
            keycloak_user.attributes = {**_attributes, item_id: permissions}
        else:
            keycloak_user.attributes = _attributes

        self.idp.update_user(keycloak_user)


async def init_keycloak(app: FastAPI, config: KeycloakSettings | None = None):
    if not hasattr(app.state, "plugins"):
        app.state.plugins = Dict()
    app.state.plugins.keycloak = KeycloakPlugin(app=app, config=config)


Keycloak = KeycloakPlugin
IDP = Keycloak


async def depends_keycloak(request: Request) -> Keycloak:
    return request.app.state.plugins.keycloak


async def depends_idp(request: Request) -> Keycloak:
    return request.app.state.plugins.keycloak


def depends_authentication(config: KeycloakSettings | None = None):
    config = config or KeycloakSettings()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.url}/realms/{config.realm}/protocol/openid-connect/token")

    async def _depends_authentication(request: Request, _=Security(oauth2_scheme)) -> OIDCUser:
        idp = (await depends_idp(request)).idp

        token = await idp.user_auth_scheme(request)
        try:
            decoded_token = idp._decode_token(token=token, options=config.options, audience="account")
        except (ExpiredSignatureError, JWTError, JWTClaimsError):
            raise HTTPException(detail="Unauthorized: token expired or invalid", status_code=401)
        user = OIDCUser.parse_obj(decoded_token)

        return user

    return _depends_authentication


async def _build_item_id(request: Request, item_id: str | list[str], in_: str | list[str]) -> str:
    body = {}
    try:
        body = await request.json()
    except json.decoder.JSONDecodeError:
        body = {}

    if isinstance(item_id, str):
        item_id = [item_id]
    if isinstance(in_, str):
        in_ = [in_]
    num_params = max([len(item_id), len(in_)])
    if len(item_id) != num_params:
        item_id *= num_params
    if len(in_) != num_params:
        in_ *= num_params
    if not (len(item_id) == len(in_)):
        raise ValueError("Parameters are cannot be parsed")

    _item_id = ""
    for name, source in zip(item_id, in_):
        param = None
        if source == "path":
            param = request.path_params.get(name)
        elif source == "query":
            param = request.query_params.get(name)
        elif source == "body":
            param = body.get(name)
        
        if param is None:
            raise HTTPException(status_code=403)
        
        _item_id = f"{_item_id}{param}:"
    _item_id = _item_id[:-1]

    if _item_id == "":
        raise HTTPException(status_code=403)

    return _item_id


def depends_permissions(
    permissions: str | callable,
    param: str | list[str] = "",
    in_: str | list[str] = "path",
    config: KeycloakSettings | None = None,
):
    config = config or KeycloakSettings()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.url}/realms/{config.realm}/protocol/openid-connect/token")

    async def check_permissions(request: Request, _=Security(oauth2_scheme)) -> OIDCUser:
        idp = (await depends_idp(request)).idp

        oidc_user = await depends_authentication(config)(request)
        user = idp.get_user(user_id=oidc_user.sub)

        if not isinstance(permissions, str):
            result = await permissions(request=request)

            if not result:
                raise HTTPException(status_code=403)

            return oidc_user

        _item_id = await _build_item_id(request, param, in_)

        user_permissions = user.attributes.get(_item_id) if user.attributes is not None else None
        if user_permissions is not None:
            user_permissions = user_permissions[0]
        else:
            user_permissions = ""

        if re.fullmatch(permissions, user_permissions) is None:
            raise HTTPException(status_code=403)

        return oidc_user
    
    return check_permissions


async def loop_(*exprs, request: Request) -> list[bool]:
    results = []
    for expr in exprs:
        try:
            await expr(request=request)
            results.append(True)
        except HTTPException:
            results.append(False)

    return results


def or_(*exprs):
    async def wrap(request: Request) -> bool:
        return any(await loop_(*exprs, request=request))

    return wrap

def and_(*exprs):
    async def wrap(request: Request) -> bool:
        return all(await loop_(*exprs, request=request))

    return wrap