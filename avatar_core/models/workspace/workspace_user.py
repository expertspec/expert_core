from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class WorkspaceUser(Base):
    __tablename__ = "workspace_user"

    workspace_id = Column(
        "workspace_id",
        ForeignKey("workspaces.workspace_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column(
        "user_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    # child-parent relationships
    workspace = relationship("Workspace", back_populates="workspace_user")
    user = relationship("User", back_populates="workspace_user")
