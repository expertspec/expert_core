import enum

from sqlalchemy import Column, Date, DateTime, ForeignKey, String, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class GenderType(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class User(Base):
    __tablename__ = "users"

    user_id = Column("user_id", ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    username = Column("username", String, nullable=False, unique=True)

    firstname = Column("firstname", String, nullable=False)
    lastname = Column("lastname", String, nullable=False)
    middlename = Column("middlename", String)

    email = Column("email", String, nullable=False)

    gender = Column("gender", String, nullable=False)
    birthday = Column("birthday", Date, nullable=False)

    photo_id = Column("photo_id", ForeignKey("attachments.attachment_id", onupdate="CASCADE", ondelete="SET NULL"))

    join_date = Column("join_date", Date, nullable=False, server_default=text("now()"))
    last_seen = Column("last_seen", DateTime, nullable=False, server_default=text("now()"))

    # child-parent relationships
    item = relationship("Item", back_populates="user")
    attachment = relationship("Attachment", back_populates="user")

    # parent-child relationships
    user_settings = relationship("UserSettings", back_populates="user", cascade="all, delete-orphan")
    user_integrations = relationship("UserIntegrations", back_populates="user", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    chat = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    message = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    chat_user = relationship("ChatUser", back_populates="user", cascade="all, delete-orphan")
    note = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    note_user = relationship("NoteUser", back_populates="user", cascade="all, delete-orphan")
    event_user = relationship("EventUser", back_populates="user", cascade="all, delete-orphan")
    task_user = relationship("TaskUser", back_populates="user", cascade="all, delete-orphan")
    news_user = relationship("NewsUser", back_populates="user", cascade="all, delete-orphan")
    workspace_user = relationship("WorkspaceUser", back_populates="user", cascade="all, delete-orphan")
    workspace_item_user = relationship("WorkspaceItemUser", back_populates="user", cascade="all, delete-orphan")
