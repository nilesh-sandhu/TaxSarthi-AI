from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from core.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # Optional Business Mapping
    # =====================================================

    business_id = Column(
        Integer,
        ForeignKey("business_profiles.id"),
        nullable=True,
        index=True,
    )

    # =====================================================
    # Government Notification Details
    # =====================================================

    title = Column(
        String(255),
        nullable=False,
    )

    message = Column(
        Text,
        nullable=False,
    )

    notification_number = Column(
        String(100),
        nullable=True,
    )

    notification_date = Column(
        DateTime,
        nullable=True,
    )

    type = Column(
        String(50),
        nullable=False,
    )  # GST | Income Tax | Customs | General

    priority = Column(
        String(20),
        default="Medium",
        nullable=False,
    )

    source = Column(
        String(255),
        default="CBIC",
        nullable=False,
    )

    applicable_to = Column(
        String(255),
        nullable=True,
    )  # Electronics, Restaurant, Textile etc.

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    expires_at = Column(
        DateTime,
        nullable=True,
    )

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
    # Relationships
    # =====================================================

    business = relationship(
        "BusinessProfile",
        lazy="joined",
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<Notification(id={self.id}, title='{self.title}')>"
        )