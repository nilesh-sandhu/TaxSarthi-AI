from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from core.database import Base


class GSTSlab(Base):

    __tablename__ = "gst_slab"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # HSN Reference
    # =====================================================

    hsn_id = Column(
        Integer,
        ForeignKey("hsn_master.id"),
        nullable=False,
        index=True,
    )

    # =====================================================
    # GST Rates
    # =====================================================

    gst_rate = Column(
        Float,
        nullable=False,
    )

    cgst = Column(
        Float,
        nullable=False,
    )

    sgst = Column(
        Float,
        nullable=False,
    )

    igst = Column(
        Float,
        nullable=False,
    )

    cess = Column(
        Float,
        default=0,
        nullable=False,
    )

    # =====================================================
    # Government Notification
    # =====================================================

    notification_no = Column(
        String(100),
        nullable=True,
    )

    effective_from = Column(
        Date,
        nullable=False,
    )

    effective_to = Column(
        Date,
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
    # Relationships
    # =====================================================

    hsn = relationship(
        "HSNMaster",
        back_populates="gst_slab",
    )

    def __repr__(self):

        return (
            f"<GSTSlab("
            f"HSN={self.hsn_id}, "
            f"GST={self.gst_rate}%)>"
        )