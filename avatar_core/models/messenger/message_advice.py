from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, text, String
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class MessageAdvice(Base):
    __tablename__ = "message_advice"
    __table_args__ = (ForeignKeyConstraint(["chat_id", "message_id"], ["messages.chat_id", "messages.message_id"]),)

    chat_id = Column("chat_id", primary_key=True)
    message_id = Column("message_id", primary_key=True)
    user_id = Column(
        "user_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    advice_id = Column(
        "advice_id",
        ForeignKey("advices.advice_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        server_default=text("null"),
    )
    emotion = Column("emotion", String, nullable=True, server_default=text("null"))

    # child-parent relationships
    chat = relationship("Message", back_populates="message_advice")
    message = relationship("Message", back_populates="message_advice")
    user = relationship("User", back_populates="message_advice")
    advice = relationship("Advice", back_populates="message_advice")
