from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class WorkspaceItemUser(Base):
    __tablename__ = "workspace_item_user"

    workspace_id = Column(
        "workspace_id",
        ForeignKey("workspaces.workspace_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    attachment_id = Column(
        "attachment_id",
        ForeignKey("attachments.attachment_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column(
        "user_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    is_liked = Column("is_liked", Boolean, nullable=False, default=False)
    is_viewed = Column("is_viewed", Boolean, nullable=False, default=False)

    # child-parent relationships
    user = relationship("User", back_populates="workspace_item_user")
    workspace = relationship("Workspace", back_populates="workspace_item_user")
    attachment = relationship("Attachment", back_populates="workspace_item_user")
