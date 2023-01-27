from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class NewsTag(Base):
    __tablename__ = "news_tag"

    news_id = Column(
        "news_id",
        ForeignKey("news.news_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id = Column(
        "tag_id",
        ForeignKey("tags.tag_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        server_default=text("null"),
    )

    # child-parent relationships
    news = relationship("News", back_populates="news_tag")
    tag = relationship("Tag", back_populates="news_tag")
