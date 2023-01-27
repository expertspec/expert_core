from sqlalchemy import Column, DateTime, ForeignKey, String, null, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    workspace_id = Column(
        "workspace_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    title = Column("title", String, nullable=False)
    description = Column("description", String, nullable=True, default=null)

    photo_id = Column(
        "photo_id",
        ForeignKey("attachments.attachment_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        default=null,
    )

    created_at = Column("created_at", DateTime, nullable=False, server_default=text("now()"))
    edited_at = Column("edited_at", DateTime, nullable=True, default=null)

    owner_id = Column("owner_id", ForeignKey("users.user_id", onupdate="CASCADE", ondelete="SET NULL"))

    # child-parent relationships
    item = relationship("Item", back_populates="workspace")

    # parent-child relationships
    workspace_user = relationship("WorkspaceUser", back_populates="workspace", cascade="all, delete-orphan")
    workspace_attachment = relationship("WorkspaceAttachment", back_populates="workspace", cascade="all, delete-orphan")
    workspace_item_user = relationship("WorkspaceItemUser", back_populates="workspace", cascade="all, delete-orphan")
