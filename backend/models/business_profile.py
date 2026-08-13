from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from core.database import Base


class BusinessProfile(Base):

    __tablename__ = "business_profiles"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # User
    # One User → Multiple Businesses
    # =====================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # =====================================================
    # Business Information
    # =====================================================

    business_name = Column(
        String(255),
        nullable=False,
    )

    owner_name = Column(
        String(255),
        nullable=False,
    )

    business_type = Column(
        String(100),
        nullable=False,
        index=True,
    )

    state = Column(
        String(100),
        nullable=False,
        index=True,
    )

    turnover = Column(
        Numeric(15, 2),
        nullable=False,
    )

    gstin = Column(
        String(15),
        unique=True,
        nullable=True,
    )

    registration_type = Column(
        String(50),
        nullable=True,
    )

    # =====================================================
    # Business Details
    # =====================================================

    interstate = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    ecommerce = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    composition_scheme = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    business_status = Column(
        String(30),
        default="Active",
        nullable=False,
    )

    # =====================================================
    # Common Fields
    # =====================================================

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
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

    user = relationship(
        "User",
        back_populates="business_profiles",
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<BusinessProfile(id={self.id}, "
            f"business_name='{self.business_name}')>"
        )
    documents = relationship(
    "Document",
    back_populates="business",
)