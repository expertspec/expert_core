from __future__ import annotations

from abc import ABC

from fastapi import FastAPI


class Plugin(ABC):
    def __init__(self, app: FastAPI | None = None, **kwargs):
        self.init()

    def init(self):
        pass

    async def on_startup(self):
        pass

    async def on_shutdown(self):
        pass
