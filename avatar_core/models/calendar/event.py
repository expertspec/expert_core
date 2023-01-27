import enum

from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Time, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class EventScope(enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    ORGANIZATION = "organization"


class EventSource(enum.Enum):
    USER = "user"
    NEWS = "news"


class Event(Base):
    __tablename__ = "events"

    event_id = Column("event_id", ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

    scope = Column("scope", String, nullable=False)

    title = Column("title", String, nullable=False)
    description = Column("description", String, nullable=True, server_default=text("null"))

    created_at = Column("created_at", DateTime, nullable=False, server_default=text("now()"))
    edited_at = Column("edited_at", DateTime, nullable=True, server_default=text("null"))

    from_date = Column("from_date", Date, nullable=False)
    from_time = Column("from_time", Time, nullable=False)
    to_date = Column("to_date", Date, nullable=True, server_default=text("null"))
    to_time = Column("to_time", Time, nullable=True, server_default=text("null"))

    location = Column("location", String, nullable=True, server_default=text("null"))

    source_type = Column("source_type", String, nullable=False)
    source = Column("source", String, nullable=True, server_default=text("null"))

    owner_id = Column(
        "owner_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        server_default=text("null"),
    )

    # child-parent relationships
    item = relationship("Item", back_populates="event", foreign_keys=[event_id])
    event_owner = relationship("Item", back_populates="event_owner", foreign_keys=[owner_id])

    # parent-child relationships
    event_user = relationship("EventUser", back_populates="event", cascade="all, delete-orphan")
    event_attachment = relationship("EventAttachment", back_populates="event", cascade="all, delete-orphan")
