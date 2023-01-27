from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class WorkspaceAttachment(Base):
    __tablename__ = "workspace_attachment"

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

    # child-parent relationships
    workspace = relationship("Workspace", back_populates="workspace_attachment")
    attachment = relationship("Attachment", back_populates="workspace_attachment")
