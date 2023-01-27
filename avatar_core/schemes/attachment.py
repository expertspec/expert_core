from __future__ import annotations

from enum import Enum

from pydantic import UUID4, BaseModel


class AddAttachmentType(str, Enum):
    FILE = "file"
    IMAGE = "image"
    URL = "url"

    NEWS = "news"
    EVENT = "event"
    MESSAGE = "message"
    NOTE = "note"


class AddAttachmentData(BaseModel):
    item_id: UUID4


class AddAttachment(BaseModel):
    item_type: AddAttachmentType
    data: AddAttachmentData

    class Config:
        use_enum_values = True


class AttachmentType(str, Enum):
    IMAGE = "image"
    DOCUMENT = "document"
    OTHER = "other"

    NEWS = "news"
    EVENT = "event"
    MESSAGE = "message"
    NOTE = "note"


class ItemAttachmentData(BaseModel):
    item_id: UUID4


class FileAttachmentData(BaseModel):
    item_id: UUID4

    filename: str | None = None
    extension: str | None = None
    size: str | None = None


class ItemAttachmentData(BaseModel):
    item_id: UUID4


class NoteAttachmentData(BaseModel):
    diary_id: UUID4
    note_id: UUID4


class Attachment(BaseModel):
    item_type: AttachmentType
    data: ItemAttachmentData | FileAttachmentData | NoteAttachmentData

    class Config:
        use_enum_values = True
