import enum

from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class PreferredMessengerType(str, enum.Enum):
    AVATAR = "avatar"
    VK = "vk"
    TELEGRAM = "telegram"
    EMAIL = "email"


class UserIntegrations(Base):
    __tablename__ = "user_integrations"

    user_id = Column("user_id", ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    preferred_messenger = Column(
        "preferred_messenger",
        String,
        nullable=False,
        server_default=text("'AVATAR'"),
    )

    vk_id = Column("vk_id", String, nullable=True)
    email = Column("email", String, nullable=False)
    telegram_id = Column("telegram_id", String, nullable=True)

    # child-parent relationships
    user = relationship("User", back_populates="user_integrations")
