
from avatar_core.models.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean, DateTime, text
from sqlalchemy.orm import relationship


class ChatUser(Base):
    __tablename__ = "chat_user"

    chat_id = Column(
        "chat_id",
        ForeignKey("chats.chat_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        "user_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    last_read_id = Column("last_read_id", Integer, nullable=False, server_default=text("-1"))

    mute_until = Column("mute_until", DateTime, nullable=True, server_default=text("null"))
    is_left = Column("is_left", Boolean, server_default=text("false"))

    # child-parent relationships
    chat = relationship("Chat", back_populates="chat_user")
    user = relationship("User", back_populates="chat_user")