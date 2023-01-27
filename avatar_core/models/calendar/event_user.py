from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class EventUser(Base):
    __tablename__ = "event_user"

    event_id = Column(
        "event_id",
        ForeignKey("events.event_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column(
        "user_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    is_liked = Column("is_liked", Boolean, nullable=False, default=False)
    is_viewed = Column("is_viewed", Boolean, nullable=False, default=False)
    is_hidden = Column("is_hidden", Boolean, nullable=False, default=False)

    is_remider_on = Column("is_remider_on", Boolean, nullable=False, default=True)
    is_sync_on = Column("is_sync_on", Boolean, nullable=False, default=True)

    # child-parent relationships
    event = relationship("Event", back_populates="event_user")
    user = relationship("User", back_populates="event_user")
