import enum

from sqlalchemy import Column, DateTime, String, MetaData, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
meta = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=meta)


class ItemType(enum.Enum):
    USER = "user"

    ORGANIZATION = "organization"

    CHAT = "chat"
    MESSAGE = "message"

    NOTE = "note"

    TASK = "task"
    EVENT = "event"

    ATTACHMENT = "attachment"

    NEWS = "news"

    WORKSPACE = "workspace"

    ADVICE = "advice"


class Item(Base):
    __tablename__ = "items"

    item_id = Column("item_id", UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    item_type = Column("item_type", String, nullable=False)

    created_at = Column("created_at", DateTime, nullable=False, server_default=text("now()"))

    # parent-child relationships
    user = relationship("User", back_populates="item", cascade="all, delete-orphan")
    subscription = relationship("Subscriber", back_populates="item", cascade="all, delete-orphan")
    organization = relationship("Organization", back_populates="item", cascade="all, delete-orphan")
    
    chat = relationship("Chat", back_populates="item", cascade="all, delete-orphan")
    message = relationship("Message", back_populates="item", cascade="all, delete-orphan")
    message_attachment = relationship("MessageAttachment", back_populates="attachment", cascade="all, delete-orphan")
    
    diary = relationship("Note", back_populates="item", cascade="all, delete-orphan")
    note = relationship("Note", back_populates="note", cascade="all, delete-orphan")
    note_attachment = relationship("NoteAttachment", back_populates="attachment", cascade="all, delete-orphan")
    
    event = relationship("Event", back_populates="item", cascade="all, delete-orphan")
    event_attachment = relationship("EventAttachment", back_populates="attachment", cascade="all, delete-orphan")
    task = relationship("Task", back_populates="item", cascade="all, delete-orphan")
    task_attachment = relationship("TaskAttachment", back_populates="attachment", cascade="all, delete-orphan")

    tag = relationship("Tag", back_populates="item", cascade="all, delete-orphan")
    news = relationship("News", back_populates="item", cascade="all, delete-orphan")
    news_attachment = relationship("NewsAttachment", back_populates="attachment", cascade="all, delete-orphan")

    attachment = relationship("Attachment", back_populates="item", cascade="all, delete-orphan")
    
    workspace = relationship("Workspace", back_populates="item", cascade="all, delete-orphan")
