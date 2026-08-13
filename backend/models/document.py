from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from core.database import Base


class Document(Base):

    __tablename__ = "documents"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    business_id = Column(
        Integer,
        ForeignKey("business_profiles.id"),
        nullable=True,
        index=True,
    )

    # =====================================================
    # Document Details
    # =====================================================

    document_name = Column(
        String(255),
        nullable=False,
    )

    document_type = Column(
        String(50),
        nullable=False,
    )
    # Invoice
    # GST Notice
    # Return
    # Certificate
    # Agreement
    # Other

    file_path = Column(
        String(500),
        nullable=False,
    )

    extracted_text = Column(
        Text,
        nullable=True,
    )

    status = Column(
        String(30),
        default="Uploaded",
        nullable=False,
    )
    # Uploaded
    # Processing
    # Completed
    # Failed

    # =====================================================
    # Timestamps
    # =====================================================

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    processed_at = Column(
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

    user = relationship(
        "User",
        back_populates="documents",
        lazy="joined",
    )

    business = relationship(
        "BusinessProfile",
        lazy="joined",
    )
    invoice_analysis = relationship(

    "InvoiceAnalysis",

    back_populates="document",

    uselist=False,

    cascade="all, delete-orphan",

    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<Document(id={self.id}, "
            f"type='{self.document_type}', "
            f"name='{self.document_name}')>"
        )