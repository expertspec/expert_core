from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base



class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column("tag_id", ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

    title = Column("title", String, nullable=True, server_default=text("null"))

    # child-parent relationships
    item = relationship("Item", back_populates="tag")

    # parent-child relationships
    news_tag = relationship("NewsTag", back_populates="tag", cascade="all, delete-orphan")