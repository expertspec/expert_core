from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class EventAttachment(Base):
    __tablename__ = "event_attachment"

    event_id = Column(
        "event_id",
        ForeignKey("events.event_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    attachment_id = Column(
        "attachment_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    # child-parent relationships
    event = relationship("Event", back_populates="event_attachment")
    attachment = relationship("Item", back_populates="event_attachment")
