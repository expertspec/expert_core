from sqlalchemy import Column, DateTime, ForeignKey, String, text, JSON
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base



class News(Base):
    __tablename__ = "news"

    news_id = Column("news_id", ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

    title = Column("title", String, nullable=True, server_default=text("null"))
    content = Column("content", String, nullable=True, server_default=text("null"))
    placeholders = Column("placeholders", JSON, nullable=True, server_default=text("null"))

    source_url = Column("source_url", String, nullable=True, server_default=text("null"))

    created_at = Column("created_at", DateTime, nullable=False, server_default=text("now()"))

    # child-parent relationships
    item = relationship("Item", back_populates="news")

    # parent-child relationships
    news_user = relationship("NewsUser", back_populates="news", cascade="all, delete-orphan")
    news_attachment = relationship("NewsAttachment", back_populates="news", cascade="all, delete-orphan")
    news_tag = relationship("NewsTag", back_populates="news", cascade="all, delete-orphan")
