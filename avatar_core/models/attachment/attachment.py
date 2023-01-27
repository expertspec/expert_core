import enum

from sqlalchemy import Column, DateTime, ForeignKey, text, String
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class AttachmentType(enum.Enum):
    IMAGE = "image"
    IMAGE_FILE = "image_file"
    DOCUMENT = "document"
    OTHER = "other"


class Attachment(Base):
    __tablename__ = "attachments"

    attachment_id = Column(
        "attachment_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    attachment_type = Column("attachment_type", String, nullable=False)

    created_at = Column("created_at", DateTime, nullable=False, server_default=text("now()"))
    edited_at = Column("edited_at", DateTime, nullable=True, server_default=text("null"))

    # child-parent relationships
    item = relationship("Item", back_populates="attachment")
