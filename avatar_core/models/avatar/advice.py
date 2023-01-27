from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class Advice(Base):
    __tablename__ = "advices"

    advice_id = Column("advice_id", ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

    emotion = Column("emotion", String, nullable=False)
    text = Column("text", String, nullable=False)

    # child-parent relationships
    item = relationship("Item", foreign_keys="Note.note_id")

    # parent-child relationships
    message_advice = relationship("MessageAdvice", back_populates="advice", cascade="all, delete-orphan")
    