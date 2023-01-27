from sqlalchemy import Boolean, Column, ForeignKey, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class TaskUser(Base):
    __tablename__ = "task_user"

    task_id = Column(
        "task_id",
        ForeignKey("tasks.task_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column(
        "user_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    is_checked = Column("is_checked", Boolean, server_default=text("false"))

    is_liked = Column("is_liked", Boolean, server_default=text("false"))
    is_viewed = Column("is_viewed", Boolean, server_default=text("false"))
    is_hidden = Column("is_hidden", Boolean, server_default=text("false"))

    is_remider_on = Column("is_remider_on", Boolean, server_default=text("true"))

    # child-parent relationships
    task = relationship("Task", back_populates="task_user")
    user = relationship("User", back_populates="task_user")
