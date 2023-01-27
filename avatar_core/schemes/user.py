from __future__ import annotations

from pydantic import BaseModel
from pydantic.types import UUID4

from avatar_core.schemes.attachment import Attachment


class UserPreview(BaseModel):
    user_id: UUID4
    username: str

    firstname: str
    lastname: str

    photo: Attachment
