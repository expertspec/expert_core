from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class NoteAttachment(Base):
    __tablename__ = "note_attachment"
    __table_args__ = (ForeignKeyConstraint(["diary_id", "note_id"], ["notes.diary_id", "notes.note_id"]),)

    diary_id = Column("diary_id", primary_key=True)
    note_id = Column("note_id", primary_key=True)
    attachment_id = Column(
        "attachment_id",
        ForeignKey("items.item_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    # child-parent relationships
    diary = relationship("Note", back_populates="note_diary_attachment", foreign_keys=[diary_id])
    note = relationship("Note", back_populates="note_attachment", foreign_keys=[note_id])
    attachment = relationship("Item", back_populates="note_attachment")
