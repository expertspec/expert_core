from sqlalchemy import Column, ForeignKey, text, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class MessageAttachment(Base):
    __tablename__ = "message_attachment"
    __table_args__ = (ForeignKeyConstraint(["chat_id", "message_id"], ["messages.chat_id", "messages.message_id"]),)

    chat_id = Column("chat_id", primary_key=True)
    message_id = Column("message_id", primary_key=True)
    attachment_id = Column(
        "attachment_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        server_default=text("null"),
    )

    # child-parent relationships
    chat = relationship("Message", back_populates="message_attachment")
    message = relationship("Message", back_populates="message_attachment")
    attachment = relationship("Item", back_populates="message_attachment")
