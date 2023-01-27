from sqlalchemy import Column, DateTime, ForeignKey, String, text
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class Note(Base):
    __tablename__ = "notes"

    diary_id = Column(
        "diary_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    note_id = Column(
        "note_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    title = Column("title", String, nullable=False)
    content = Column("content", String, nullable=True, server_default=text("NULL"))

    created_at = Column("created_at", DateTime, nullable=False, server_default=text("now()"))
    edited_at = Column("edited_at", DateTime, nullable=True, server_default=text("NULL"))

    creator_id = Column(
        "creator_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    # child-parent relationships
    item = relationship("Item", back_populates="diary", foreign_keys=[diary_id])
    note = relationship("Item", back_populates="note", foreign_keys=[note_id])
    user = relationship("User", back_populates="note")

    # parent-child relationships
    note_diary_user = relationship("NoteUser", back_populates="diary", cascade="all, delete-orphan")
    note_user = relationship("NoteUser", back_populates="note", cascade="all, delete-orphan")
    note_diary_attachment = relationship("NoteAttachment", back_populates="diary", cascade="all, delete-orphan")
    note_attachment = relationship("NoteAttachment", back_populates="note", cascade="all, delete-orphan")
