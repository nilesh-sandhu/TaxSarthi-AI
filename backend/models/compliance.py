from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
)

from core.database import Base


class Compliance(Base):

    __tablename__ = "compliance"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    compliance_type = Column(
        String(100),
        nullable=False,
    )

    due_days = Column(
        Integer,
        nullable=True,
    )

    priority = Column(
        String(20),
        default="Medium",
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):

        return f"<Compliance(title='{self.title}')>"