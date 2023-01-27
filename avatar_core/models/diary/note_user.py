from sqlalchemy import Boolean, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class NoteUser(Base):
    __tablename__ = "note_user"
    __table_args__ = (ForeignKeyConstraint(["diary_id", "note_id"], ["notes.diary_id", "notes.note_id"]),)

    diary_id = Column("diary_id", primary_key=True)
    note_id = Column("note_id", primary_key=True)
    user_id = Column(
        "user_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    is_liked = Column("is_liked", Boolean, nullable=False, default=False)
    is_viewed = Column("is_viewed", Boolean, nullable=False, default=False)
    is_hidden = Column("is_hidden", Boolean, nullable=False, default=False)

    # child-parent relationships
    diary = relationship("Note", back_populates="note_diary_user", foreign_keys=[diary_id])
    note = relationship("Note", back_populates="note_user", foreign_keys=[note_id])
    user = relationship("User", back_populates="note_user")
