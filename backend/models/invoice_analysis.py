from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Float,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from core.database import Base


class InvoiceAnalysis(Base):

    __tablename__ = "invoice_analysis"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # Reference
    # =====================================================

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
        index=True,
    )

    # =====================================================
    # Invoice Details
    # =====================================================

    invoice_number = Column(
        String(100),
        nullable=True,
    )

    supplier = Column(
        String(255),
        nullable=True,
    )

    gstin = Column(
        String(20),
        nullable=True,
    )

    invoice_date = Column(
        String(50),
        nullable=True,
    )

    total_amount = Column(
        Float,
        nullable=True,
    )

    # =====================================================
    # AI Results
    # =====================================================

    risk_score = Column(
        Integer,
        default=100,
    )

    validation_status = Column(
        String(50),
        default="Pending",
    )

    recommendations = Column(
        Text,
        nullable=True,
    )

    errors = Column(
        Text,
        nullable=True,
    )

    # =====================================================
    # Timestamp
    # =====================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # =====================================================
    # Relationship
    # =====================================================

    document = relationship(

    "Document",

    back_populates="invoice_analysis",

    lazy="joined",

    )

    def __repr__(self):

        return (
            f"<InvoiceAnalysis(id={self.id}, "
            f"invoice='{self.invoice_number}')>"
        )