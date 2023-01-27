from sqlalchemy import Boolean, Column, ForeignKey, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id = Column("user_id", ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    is_avatar_suggestions_allowed = Column("is_avatar_suggestions_allowed", Boolean, server_default=text("true"))
    is_sync_calendar_allowed = Column("is_sync_calendar_allowed", Boolean, server_default=text("false"))
    is_profile_sharing_allowed = Column("is_profile_sharing_allowed", Boolean, server_default=text("true"))

    # child-parent relationships
    user = relationship("User", back_populates="user_settings")
