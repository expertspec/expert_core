import enum

from sqlalchemy import Column, DateTime, ForeignKey, String, text, JSON
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class ChatType(enum.Enum):
    GLOBAL = "global"
    PERSONAL = "personal"
    GROUP = "group"
    WORKSPACE = "workspace"
    AVATAR = "avatar"


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column("chat_id", ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    chat_type = Column("chat_type", String, nullable=False)

    name = Column("name", String, unique=True, nullable=False)

    title = Column("title", String, nullable=True, server_default=text("null"))
    description = Column("description", String, nullable=True, server_default=text("null"))
    placeholders = Column("placeholders", JSON, nullable=True, server_default=text("null"))

    owner_id = Column(
        "owner_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        server_default=text("null"),
    )

    photo_id = Column(
        "photo_id",
        ForeignKey("attachments.attachment_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        server_default=text("null"),
    )

    created_at = Column("created_at", DateTime, nullable=False, server_default=text("now()"))

    # child-parent relationships
    item = relationship("Item", back_populates="chat")
    owner = relationship("Item", back_populates="chat_owner")
    attachment = relationship("Attachment", back_populates="chat")

    # parent-child relationships
    chat_user = relationship("ChatUser", back_populates="chat", cascade="all, delete-orphan")
    message = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    message_attachment = relationship("MessageAttachment", back_populates="chat", cascade="all, delete-orphan")
    message_advice = relationship("MessageAdvice", back_populates="chat", cascade="all, delete-orphan")