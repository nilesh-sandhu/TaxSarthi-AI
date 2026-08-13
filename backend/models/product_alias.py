from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from core.database import Base


class ProductAlias(Base):

    __tablename__ = "product_alias"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # Product Reference
    # =====================================================

    product_id = Column(
        Integer,
        ForeignKey("product_master.id"),
        nullable=False,
        index=True,
    )

    # =====================================================
    # Alias
    # =====================================================

    alias = Column(
        String(255),
        unique=True,
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
    # Relationship
    # =====================================================

    product = relationship(
        "ProductMaster",
        back_populates="aliases",
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<ProductAlias(alias='{self.alias}')>"
        )