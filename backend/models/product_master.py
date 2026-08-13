from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from core.database import Base


class ProductMaster(Base):

    __tablename__ = "product_master"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # Product Information
    # =====================================================

    product_name = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    # =====================================================
    # HSN
    # =====================================================

    hsn_code = Column(
        String(20),
        ForeignKey("hsn_master.hsn_code"),
        nullable=True,
        index=True,
    )

    # =====================================================
    # GST RATE
    # =====================================================

    gst_rate = Column(
        Float,
        nullable=True,
    )

    # =====================================================
    # Description
    # =====================================================

    description = Column(
        Text,
        nullable=True,
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

    category = relationship(
        "Category",
        back_populates="products",
    )

    hsn = relationship(
        "HSNMaster",
        back_populates="products",
    )

    aliases = relationship(
        "ProductAlias",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<ProductMaster("
            f"id={self.id}, "
            f"product_name='{self.product_name}', "
            f"hsn='{self.hsn_code}', "
            f"gst={self.gst_rate}"
            f")>"
        )