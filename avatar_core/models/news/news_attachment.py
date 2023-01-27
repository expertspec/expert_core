from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class NewsAttachment(Base):
    __tablename__ = "news_attachment"

    news_id = Column(
        "news_id",
        ForeignKey("news.news_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    attachment_id = Column(
        "attachment_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        server_default=text("null"),
    )

    # child-parent relationships
    news = relationship("News", back_populates="news_attachment")
    attachment = relationship("Item", back_populates="news_attachment")
