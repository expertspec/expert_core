from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class TaskAttachment(Base):
    __tablename__ = "task_attachment"

    task_id = Column(
        "task_id",
        ForeignKey("tasks.task_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    attachment_id = Column(
        "attachment_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    # child-parent relationships
    task = relationship("Task", back_populates="task_attachment")
    attachment = relationship("Item", back_populates="task_attachment")
