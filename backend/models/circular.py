from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    String,
    Text,
)

from core.database import Base


class Circular(Base):

    __tablename__ = "circulars"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # Circular Details
    # =====================================================

    circular_no = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    title = Column(
        String(500),
        nullable=False,
    )

    subject = Column(
        String(500),
        nullable=True,
    )

    description = Column(
        Text,
        nullable=False,
    )

    issue_date = Column(
        Date,
        nullable=False,
    )

    reference = Column(
        String(500),
        nullable=True,
    )

    # =====================================================
    # Status
    # =====================================================

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    # =====================================================
    # Audit
    # =====================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<Circular("
            f"circular_no='{self.circular_no}')>"
        )