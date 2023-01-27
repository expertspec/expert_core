import enum

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, Time, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class TaskIcon(enum.Enum):
    WORK = "work"
    ANIMAL = "animal"
    STUDY = "study"
    ENTERTAINMENT = "entertainment"
    SPIRITUAL = "spiritual"
    SPORT = "sport"
    HEALTH = "health"
    PEOPLE = "people"
    PERSONAL = "personal"
    NATURE = "nature"
    HOME = "home"
    EAT = "eat"


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column("task_id", ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    parent_task_id = Column(
        "parent_task_id",
        ForeignKey("tasks.task_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        server_default=text("null"),
    )

    title = Column("title", String, nullable=False)
    content = Column("content", String, nullable=True, server_default=text("null"))

    icon = Column("icon", String, nullable=False)

    created_at = Column("created_at", DateTime, nullable=False, server_default=text("now()"))
    edited_at = Column("edited_at", DateTime, nullable=True, server_default=text("null"))

    from_date = Column("from_date", Date, nullable=True, server_default=text("null"))
    from_time = Column("from_time", Time, nullable=True, server_default=text("null"))
    to_date = Column("to_date", Date, nullable=True, server_default=text("null"))
    to_time = Column("to_time", Time, nullable=True, server_default=text("null"))

    location = Column("location", String, nullable=True, server_default=text("null"))

    is_postponable = Column("is_postponable", Boolean, server_default=text("false"))

    owner_id = Column(
        "owner_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        server_default=text("null"),
    )

    # child-parent relationships
    item = relationship("Item", back_populates="task", foreign_keys=[task_id])
    task_owner = relationship("Item", back_populates="task_owner", foreign_keys=[owner_id])

    # parent-child relationships
    task_user = relationship("TaskUser", back_populates="task", cascade="all, delete-orphan")
    task_attachment = relationship("TaskAttachment", back_populates="task", cascade="all, delete-orphan")
