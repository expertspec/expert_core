from sqlalchemy import Boolean, Column, DateTime, ForeignKey, ForeignKeyConstraint, text, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (ForeignKeyConstraint(["chat_id", "reply_to"], ["messages.chat_id", "messages.message_id"]),)

    chat_id = Column(
        "chat_id",
        ForeignKey("chats.chat_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    message_id = Column(
        "message_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column("user_id", ForeignKey("users.user_id", ondelete="SET NULL"))

    reply_to = Column("reply_to", UUID, nullable=True, server_default=text("null"))

    created_at = Column("created_at", DateTime, nullable=False, server_default=text("now()"))
    edited_at = Column("edited_at", DateTime, nullable=True, server_default=text("null"))

    content = Column("content", String, nullable=True, server_default=text("null"))
    placeholders = Column("placeholders", JSON, nullable=True, server_default=text("null"))

    is_pinned = Column("is_pinned", Boolean, server_default=text("false"))

    # child-parent relationships
    chat = relationship("Chat", back_populates="message")
    user = relationship("User", back_populates="message")

    # parent-child relationships
    message_attachment = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")
    message_advice = relationship("MessageAdvice", back_populates="message", cascade="all, delete-orphan")
