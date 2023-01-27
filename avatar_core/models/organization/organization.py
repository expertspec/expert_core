from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(
        "organization_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    title = Column("title", String, nullable=False)

    # child-parent relationships
    item = relationship("Item", back_populates="organization")

    # parent-child relationships
    organization_user = relationship("OrganizationUser", back_populates="organization", cascade="all, delete-orphan")
