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


class HSNMaster(Base):

    __tablename__ = "hsn_master"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # HSN Details
    # =====================================================

    hsn_code = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    description = Column(
        Text,
        nullable=False,
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
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
    # Relationships
    # =====================================================

    category = relationship(
        "Category",
        back_populates="hsn_codes",
    )

    gst_slab = relationship(
        "GSTSlab",
        back_populates="hsn",
        uselist=False,
    )

    products = relationship(
        "ProductMaster",
        back_populates="hsn",
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<HSNMaster("
            f"hsn_code='{self.hsn_code}')>"
        )