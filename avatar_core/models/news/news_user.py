
from avatar_core.models.base import Base
from sqlalchemy import Column, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship


class NewsUser(Base):
    __tablename__ = "news_user"

    news_id = Column(
        "news_id",
        ForeignKey("news.news_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        "user_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    is_hidden = Column("is_hidden", Boolean, server_default=text("false"))
    is_viewed = Column("is_viewed", Boolean, server_default=text("false"))
    is_liked = Column("is_liked", Boolean, server_default=text("false"))

    # child-parent relationships
    news = relationship("News", back_populates="news_user")
    user = relationship("User", back_populates="news_user")