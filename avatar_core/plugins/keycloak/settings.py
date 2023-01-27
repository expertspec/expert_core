from __future__ import annotations

from pydantic import BaseSettings


class KeycloakSettings(BaseSettings):
    protocol: str = "http"
    host: str = "localhost"
    port: int | None = None
    http_relative_path: str = "/"

    realm: str
    client_id: str
    client_secret: str
    admin_client_id: str
    admin_client_secret: str
    verify_signature: bool = True

    timeout: int = 10

    class Config:
        env_prefix: str = "keycloak_"
        env_file: str = ".env"
        allow_mutation: bool = False

    @property
    def url(self):
        _port = f":{self.port}" if self.port is not None else ""

        return f"{self.protocol}://{self.host}{_port}{self.http_relative_path}"

    @property
    def callback_uri(self):
        _port = f":{self.port}" if self.port is not None else ""

        return f"{self.protocol}://{self.host}{_port}/callback"

    @property
    def opts(self):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "admin_client_id": self.admin_client_id,
            "admin_client_secret": self.admin_client_secret,
            "realm": self.realm,
        }

    @property
    def options(self):
        if self.verify_signature:
            return {
                "verify_signature": False,
                "verify_aud": True,
                "veryfy_exp": False,
            }