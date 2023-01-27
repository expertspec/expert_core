from __future__ import annotations

from enum import Enum

from pydantic import UUID4, BaseModel


class PlaceholderType(str, Enum):
    URL = "url"
    AT = "at"


class UrlPlaceholderData(BaseModel):
    url: str
    replacement_text: str | None = None


class AtPlaceholderData(BaseModel):
    user_id: UUID4
    replacement_text: str | None = None


class Placeholder(BaseModel):
    placeholder_type: PlaceholderType
    data: AtPlaceholderData | UrlPlaceholderData

    class Config:
        use_enum_values = True


class Content(BaseModel):
    template: str
    placeholders: list[Placeholder] = []
