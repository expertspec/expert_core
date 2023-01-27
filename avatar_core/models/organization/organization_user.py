import enum

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from avatar_core.models.base import Base


class AssignationType(enum.Enum):
    WORK = "work"
    STUDY = "study"


class OrganizationUser(Base):
    __tablename__ = "organization_user"

    organization_id = Column(
        "organization_id",
        ForeignKey("organizations.organization_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column(
        "user_id",
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    idx = Column("idx", Integer, primary_key=True)

    assignation_type = Column("assignation_type", String, nullable=False)

    # work - department
    # study - faculty
    department = Column("department", String, nullable=True)
    # study - degree: bachelor, master, phd
    degree = Column("degree", String, nullable=True)
    # work - role
    # study - specialization
    role = Column("role", String, nullable=True)
    # work - grade: junior, middle, senior
    # study - year
    grade = Column("grade", String, nullable=True)
    # work - team
    # study - group
    team = Column("team", String, nullable=True)

    assigned_on = Column("assigned_on", Date, nullable=True)
    discharged_on = Column("discharged_on", Date, nullable=True)

    # child-parent relationships
    organization = relationship("Organization", back_populates="organization_user")
    user = relationship("User", back_populates="organization_user")
