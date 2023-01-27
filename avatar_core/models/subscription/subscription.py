from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(
        "subscription_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    subscriber_id = Column(
        "subscriber_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    # child-parent relationships
    item = relationship("Item", foreign_keys=[subscription_id])
    user = relationship("User", foreign_keys=[subscriber_id])
